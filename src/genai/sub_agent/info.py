from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from genai.models import MetaInfo
import time
from pathlib import Path
from genai.sub_agent.base_sub_agent import BaseSubAgent
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class InfoAgentState(TypedDict):
    messages: Annotated[List, add_messages]
    data: MetaInfo


class InfoAgent(BaseSubAgent):
    def __init__(self, llm_instance):
        super().__init__(llm_instance=llm_instance)

    def _get_state(self):
        return InfoAgentState(messages=[], data=None)

    def _get_sys_prompt_path(self) -> Path:
        base_path = Path(__file__).parent.parent.parent.parent / "data" / "system_prompt"
        return base_path / "info.json"

    def _create_default_model(self) -> MetaInfo:
        """Create a default Info object with empty values."""
        return MetaInfo(
            title="",
            description=None,
            owner=None,
            contact=None
        )
    
    def generate_object_node(self, state: InfoAgentState) -> InfoAgentState:
        sys_prompt = self._system_prompt.get("create_object")
        human_requests = [
            request for request in state.get("messages") if isinstance(request, HumanMessage)
        ]
        messages = [SystemMessage(content=sys_prompt)] + human_requests
        parser = JsonOutputParser(pydantic_object=MetaInfo)
        max_retries = 3
        
        for attempt in range(max_retries):
            response = self._llm.invoke(messages)
            time.sleep(30)
            try:  
                draw_data = parser.parse(response.content).get("metainfo", {})
                logger.info(response.content)
                data = super().normalize_and_validate(MetaInfo, draw_data)
                if data:
                    state["data"] = data
                    return state
            except Exception:
                if attempt == max_retries - 1:
                    break
        
        # If all retries failed or no valid data found, set default Info
        state["data"] = self._create_default_model()
        return state

    @staticmethod
    def post_processing_data(draw_data: Dict[str, Any], except_data_model_class):
        object_fields = set(except_data_model_class.model_fields.keys())

        filtered_data = {}

        for field_name in object_fields:
            if field_name in draw_data:
                filtered_data[field_name] = draw_data[field_name]

        try:
            return except_data_model_class(**filtered_data)
        except Exception as e:
            print(f"Error: {e}")
            return None

    def _create_graph(self):
        graph_builder = StateGraph(InfoAgentState)
        graph_builder.add_node("generate_data", self.generate_object_node)
        graph_builder.add_edge("generate_data", END)

        graph_builder.set_entry_point("generate_data")
        graph = graph_builder.compile()
        return graph
    