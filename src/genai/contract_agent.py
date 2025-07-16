from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Union, List
from root_model import DataContract
from langgraph.prebuilt import create_react_agent


class State(TypedDict):
    messages: Annotated[list, add_messages]
    data_contract: Union[DataContract, None]



    