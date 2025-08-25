from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from genai.models import DataContractModels, ModelDef, FieldDef
import time
from pathlib import Path
from genai.sub_agent.base_sub_agent import BaseSubAgent


import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class DataModelAgentState(TypedDict):
    messages: Annotated[List, add_messages]
    data: DataContractModels


class DataModelAgent(BaseSubAgent):
    def __init__(self, llm_instance):
        super().__init__(llm_instance=llm_instance)

    def _get_state(self):
        return DataModelAgentState(messages=[], data=None)

    def _get_sys_prompt_path(self) -> Path:
        base_path = Path(__file__).parent.parent.parent.parent / "data" / "system_prompt"
        return base_path / "model.json"

    def _create_default_model(self) -> DataContractModels:
        return DataContractModels(
            data_models = {
                "sample_field_keys": ModelDef(
                    type="table",
                    description="sample_description",
                    fields={
                        "sample_data_field": FieldDef(
                            type="text",
                            description="sample_description for data field"
                        )
                    }
                )
            }
        )

    
    def generate_object_node(self, state: DataModelAgentState) -> DataModelAgentState:
        sys_prompt = self._system_prompt.get("create_object")
        human_requests = [request for request in state.get("messages") if isinstance(request, HumanMessage)]
        messages = [SystemMessage(content=sys_prompt)] + human_requests
        parser = JsonOutputParser(pydantic_object=DataContractModels)
        max_retries = 3
        for attempt in range(max_retries):
            response = self._llm.invoke(messages)
            time.sleep(30)
            try:
                draw_data = parser.parse(response.content).get("models", {})
                if draw_data:
                    data = self.post_processing_data(draw_data=draw_data)
                    state["data"] = data
                return state
            except Exception:
                if attempt == max_retries - 1:
                    data = {}
                    return state
        return state

    @staticmethod
    def post_processing_data(draw_data: Dict[str, Any]):
        model_def_object_fields = set(ModelDef.model_fields.keys())
        field_def_object_fields = set(FieldDef.model_fields.keys())

        all_data = {}

        for key, item in draw_data.items():
            filtered_data = {}

            for field_name in model_def_object_fields:
                if field_name in item:
                    if not field_name == "fields":
                        filtered_data[field_name] = item[field_name]
            if not isinstance(item['fields'], dict):    
                for sub_key, sub_item in item['fields']:
                    sub_filtered_data = {}

                    for sub_field_name in field_def_object_fields:
                        if sub_field_name in sub_item:
                            sub_filtered_data[sub_field_name] = sub_item[sub_field_name]

                    try:
                        sub_processed_data = {sub_key: FieldDef(**sub_filtered_data)}
                    except:
                        print(f'Error: {e}')
                        sub_processed_data = {sub_key: None}
                    filtered_data['fields'].update(sub_processed_data)
            else:
                filtered_data['fields'] = {"sample_data_fields": FieldDef(type="text", description="sample data")}
            
            try:
                processed_data = {key: ModelDef(**filtered_data)}
            except Exception as e:
                print(f'Error: {e}')
                processed_data = {key: None}

            all_data.update(processed_data)

        return DataContractModels(data_models=all_data)


    def _create_graph(self):
        graph_builder = StateGraph(DataModelAgentState)
        graph_builder.add_node("generate_data", self.generate_object_node)
        graph_builder.add_edge("generate_data", END)

        graph_builder.set_entry_point("generate_data")
        graph = graph_builder.compile()
        return graph