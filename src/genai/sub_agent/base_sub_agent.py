from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Union, Dict
from genai.models import DefinitionObject
from langchain_core.messages import HumanMessage


class SubState(TypedDict):
    messages: Annotated[list, add_messages]
    data: Union[DefinitionObject, None]


class BaseSubAgent:
    def __init__(self, llm_instance):
        self._graph = self._create_graph()
        self._llm = llm_instance
        self._system_prompt: Dict[str, str] = self._load_system_prompt()

    def _load_system_prompt(self):
        pass

    def generate_object_node(self, state: SubState):
        pass
    
    def _create_graph(self):
        graph_builder = StateGraph(SubState)
        graph_builder.add_node("create_object", self.generate_object_node)
        graph_builder.add_edge(START, "create_object")

        graph_builder.add_edge("create_object", END)
        graph = graph_builder.compile()
        return graph
    
    def invoke(self, user_query):
        state = SubState(messages=[HumanMessage(content=user_query)])
        rs = self._graph.invoke(state)
        return rs


