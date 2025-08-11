from typing import List
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from genai.models import Terms
import time
from pathlib import Path
from genai.sub_agent.base_sub_agent import BaseSubAgent


class TermsAgentState(TypedDict):
    messages: Annotated[List, add_messages]
    data: Terms


class TermsAgent(BaseSubAgent):
    def __init__(self, llm_instance):
        super().__init__(llm_instance=llm_instance)

    def _get_state(self):
        return TermsAgentState(messages=[], data=None)

    def _get_sys_prompt_path(self) -> Path:
        base_path = Path(__file__).parent.parent.parent.parent / "data" / "system_prompt"
        return base_path / "terms.json"

    def _create_default_model(self) -> Terms:
        return Terms()

    def generate_object_node(self, state: TermsAgentState) -> TermsAgentState:
        sys_prompt = self._system_prompt.get("create_object")
        human_requests = [
            req for req in state.get("messages") if isinstance(req, HumanMessage)
        ]
        messages = [SystemMessage(content=sys_prompt)] + human_requests
        parser = JsonOutputParser(pydantic_object=Terms)
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                response = self._llm.invoke(messages)
                time.sleep(20)

                draw_data = parser.parse(response.content).get("terms", {})

                if not draw_data:
                    raise ValueError("Parsed data is empty.")
                
                state['data'] = super().normalize_and_validate(Terms, draw_data)
                return state
            
            except Exception as e:
                print(f"Agent terms [Attempt {attempt}/{max_retries}] Error: {e}")
                if attempt < max_retries:
                    print("Retrying...\n")

        print("Max retries reached. Using default model.")
        state["data"] = self._create_default_model()
        return state

    def _create_graph(self):
        graph_builder = StateGraph(TermsAgentState)
        graph_builder.add_node("generate_data", self.generate_object_node)
        graph_builder.add_edge("generate_data", END)

        graph_builder.set_entry_point("generate_data")
        graph = graph_builder.compile()
        return graph