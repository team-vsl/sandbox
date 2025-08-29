from typing import List
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
                parsed = parser.parse(response.content)

                if isinstance(parsed, dict) and "data_models" in parsed:
                    payload = parsed
                elif isinstance(parsed, dict) and "models" in parsed:
                    payload = {"data_models": parsed.get("models", {})}
                elif isinstance(parsed, dict):
                    payload = {"data_models": parsed}
                else:
                    payload = {"data_models": {}}

                logging.info(payload.get("data_models"))
                logging.info(type(payload.get("data_models")))
                data = super().normalize_and_validate(DataContractModels, payload)

                if data:
                    state["data"] = data.data_models
                return state
            except Exception as e:
                print(e)
                if attempt == max_retries - 1:
                    break
        state["data"] = self._create_default_model()
        return state

    def _create_graph(self):
        graph_builder = StateGraph(DataModelAgentState)
        graph_builder.add_node("generate_data", self.generate_object_node)
        graph_builder.add_edge("generate_data", END)

        graph_builder.set_entry_point("generate_data")
        graph = graph_builder.compile()
        return graph