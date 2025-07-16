from typing import List, Dict
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from typing import TypedDict, Annotated, Union
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from . import sub_agent
import time


class State(TypedDict):
    messages: Annotated[list, add_messages]
    # data_contract: Union[DataContract, None]
    worker_agent: list
    data_contract: list


class ContractAgent:
    def __init__(self, llm_instance):
        self._llm = llm_instance
        self._data = None
        self._graph = self._create_graph()

    def detect_intent(self, user_input: HumanMessage) -> str:

        with open("/var/vpbank/datacontracts/sandbox/data/system_prompt/root_agent.txt", "r", encoding="utf-8")  as fp:
            classification_prompt = fp.read()

        message = [
            SystemMessage(content=classification_prompt),
            user_input
        ]
        response = self._llm.invoke(message)

        time.sleep(60)

        return response
    
    def detect_intent_node(self, state: State) -> State:
        input_text = state.get("messages")[-1]

        if not isinstance(input_text, HumanMessage):
            return state

        worker_agent_posible = ["data_model", "definitions", "info", "server", "servicelevels", "terms"]
        response = self.detect_intent(input_text)
        parser = CommaSeparatedListOutputParser()
        worker_agent = parser.parse(response.content)

        for item in worker_agent:
            if item not in worker_agent_posible:
                state['error'] = "Error with detect worker_agent: {worker_agent}".format(worker_agent=worker_agent)
                return state

        state['worker_agent'] = worker_agent
        return state
    
    def agent_call(self, state: State) -> State:
        worker_agent_list = state['worker_agent']
        
        agent_list = []

        for agent_item in worker_agent_list:
            if agent_item == "data_model":
                agent_instance = sub_agent.DataModelAgent(self._llm)
                agent_list.append(agent_instance)
            elif agent_item == "definitions":
                agent_instance = sub_agent.DefinitionsAgent(self._llm)
                agent_list.append(agent_instance)
            elif agent_item == "info":
                agent_instance = sub_agent.InfoAgent(self._llm)
                agent_list.append(agent_instance)
            elif agent_item == "server":
                agent_instance = sub_agent.ServerAgent(self._llm)
                agent_list.append(agent_instance)
            elif agent_item == "servicelevels":
                agent_instance = sub_agent.ServiceLevelsAgent(self._llm)
                agent_list.append(agent_instance)
            elif agent_item == "terms":
                agent_instance = sub_agent.TermsAgent(self._llm)
                agent_list.append(agent_instance)
            else:
                state['error'] = "Error with worker_agent: {worker_agent}".format(worker_agent=agent)
                return state
        
        message = state.get("messages")[-1].content
        
        data_contract = []

        for agent in agent_list:
 
            agent_response = agent.invoke(message)
            time.sleep(60)
            data_contract.append(agent_response.get("data"))
        state['data_contract'] = data_contract
        return state
    
    def _create_graph(self):
        graph_builder = StateGraph(State)
        graph_builder.add_node("detect_intent_node", self.detect_intent_node)
        graph_builder.add_node("agent_call", self.agent_call)
        graph_builder.add_edge("detect_intent_node", "agent_call")
        graph_builder.add_edge("agent_call", END)

        graph_builder.set_entry_point("detect_intent_node")
        graph = graph_builder.compile()
        return graph

    def invoke(self, user_query):
        state = State(messages=[HumanMessage(content=user_query)])
        rs = self._graph.invoke(state)
        return rs
                        