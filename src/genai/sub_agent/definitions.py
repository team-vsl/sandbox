from typing import List, Dict
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import JsonOutputParser
from typing import TypedDict, Annotated, Union
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from genai.models import DefinitionObject


class DefinitionAgentState(TypedDict):
    messages: Annotated[List, add_messages]
    data: Union[DefinitionObject, None]


class DefinitionField(BaseModel):
    info: DefinitionObject


class DefinitionsAgent:
    def __init__(self, llm_instance):
        self._graph = self._create_graph()
        self._llm = llm_instance
        self._system_prompt: Dict[str, str] = self._load_system_prompt()

    @staticmethod
    def _load_system_prompt():
        with open("/var/vpbank/datacontracts/sandbox/data/system_prompt/definitions.txt", "r", encoding="utf-8") as fp:
            data = fp.read()
        return {"create_object": data}

    def generate_object_node(self, state: DefinitionAgentState) -> DefinitionAgentState:
        sys_prompt = self._system_prompt.get("create_object")
        human_request = state.get("messages")[-1]

        if not isinstance(human_request, HumanMessage):
            return state
        
        messages = [SystemMessage(content=sys_prompt), human_request]
        parser = JsonOutputParser(pydantic_object=DefinitionField)
        response = self._llm.invoke(messages)
        state["data"] = parser.parse(response.content)
        return state

    def _create_graph(self):
        graph_builder = StateGraph(DefinitionAgentState)
        graph_builder.add_node("generate_data", self.generate_object_node)
        graph_builder.add_edge("generate_data", END)

        graph_builder.set_entry_point("generate_data")
        graph = graph_builder.compile()
        return graph
    
    def invoke(self, user_query):
        state = DefinitionAgentState(messages=[HumanMessage(content=user_query)])
        rs = self._graph.invoke(state)
        return rs