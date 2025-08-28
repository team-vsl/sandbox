from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from typing import TypedDict, Annotated, Dict, List
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from . import sub_agent
import time
from pathlib import Path
from .root_model import DataContract
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    worker_agent: list
    data_contract: DataContract
    required_info: dict
    error: str


class DataContractAgent:
    def __init__(self, llm_instance, data_contract:Dict = None):
        self._llm = llm_instance
        self._worker_agents = self._init_worker_agents()
        self._sys_prompt = self._get_sys_prompt()
        self._graph = self._create_graph()

        if data_contract:
            self._state = State(messages=[], worker_agent=[], data_contract=data_contract, check_intent_message="", error="")
        else:
            self._state = State(messages=[], worker_agent=[], data_contract=self._create_default_data_contract(), check_intent_message="", error="")
        
    @staticmethod
    def _create_default_data_contract():
        """Create a default DataServer object with empty values."""
        return {"id": None, "metainfo": None, "server": None, "terms": None, "data_models": None, "servicelevels": None}

    def _get_sys_prompt_path(self) -> Path:
        base_path = Path(__file__).parent.parent.parent / "data" / "system_prompt"
        return base_path / "master.json"

    def _get_sys_prompt(self) -> Dict[str, str]:
        sys_prompt_path = self._get_sys_prompt_path()   

        try:
            with open(sys_prompt_path, "r", encoding="utf-8") as fp:
                sys_prompt = json.load(fp)
        except Exception as e:
            sys_prompt = {}
            print(f"Warning: Cannot read JSON file {sys_prompt_path}: {e}")
        return sys_prompt


    def _init_worker_agents(self):
        return {
            "metainfo": sub_agent.InfoAgent(self._llm),
            "data_models": sub_agent.DataModelAgent(self._llm),
            "server": sub_agent.ServerAgent(self._llm),
            "servicelevels": sub_agent.ServiceLevelsAgent(self._llm),
            "terms": sub_agent.TermsAgent(self._llm),
        }

    def _change_create_to_update_pq(self, sub_agent_name:str, user_input:List[BaseMessage]):

        last_user_input = user_input[-1]
        if not isinstance(last_user_input, HumanMessage):
            return user_input
        data = self._state['data_contract'].get(sub_agent_name)     

        update_str = last_user_input.content + f"\nUpdate the contract based on this data: \n{data}"
        updated_user_input = user_input[:-1] + [HumanMessage(content=update_str)]
        return updated_user_input
        
    @staticmethod
    def _flatten_output_data(model_instance):
        if not isinstance(model_instance, dict) and not isinstance(model_instance, list):
            return model_instance.model_dump()

        if isinstance(model_instance, list):
            return [data.model_instance for data in model_instance]

        if isinstance(model_instance, dict):
            return {key:value.model_dump() for key, value in model_instance.items()}
        
        return model_instance

    def choose_worker_fn(self, user_inputs: list) -> str:
        classification_prompt = self._sys_prompt["choose_worker_agent_node"]
        message = [
            SystemMessage(content=classification_prompt),
            *user_inputs
        ]

        logging.info("Choose worker agent running")
        response = self._llm.invoke(message)
        time.sleep(20)
        return response

    def post_response_node(self, state: State) -> State:
        messages = state.get("messages", [])
        user_inputs = [msg for msg in messages if isinstance(msg, HumanMessage)][-3:]
        if not user_inputs:
            return state

        post_response_prompt = self._sys_prompt["post_response"]
        logging.info("Post response processing")

        messages = [
            SystemMessage(content=post_response_prompt), user_inputs[-1]
        ]

        response = self._llm.invoke(messages)
        time.sleep(20)

        logging.info("\n" + response.content)
        state['messages'].append(AIMessage(content=response.content))

        return state

    def choose_worker_agent_node(self, state: State) -> State:
        messages = state.get("messages", [])

        user_inputs = [msg for msg in messages if isinstance(msg, HumanMessage)][-1:]
        if not user_inputs:
            return state
        worker_agent_posible = ["data_models", "metainfo", "server", "servicelevels", "terms"]
        response = self.choose_worker_fn(user_inputs)
        parser = CommaSeparatedListOutputParser()
        try:
            worker_agent = parser.parse(response.content)
        except Exception as e:
            state['error'] = f"Error parsing worker_agent: {e}"
            return state

        if not worker_agent:
            state['error'] = "No worker_agent detected from LLM response."

        for item in worker_agent:
            if item not in worker_agent_posible:
                state['error'] = f"Error with detect worker_agent: {worker_agent}"
                
        state['worker_agent'] = worker_agent
        return state


    def agent_call_node(self, state: State) -> State:
        user_input = state.get("messages")
        current_data_contract = state.get("data_contract")
        
        worker_agents = state.get("worker_agent", [])
        results = {}
        for agent_name in worker_agents:
            agent = self._worker_agents.get(agent_name)
            if agent is None:
                state['error'] = f"Không tìm thấy agent cho worker_agent: {agent_name}"
                continue

            logging.info(f"Agent {agent_name} running \n")

            if current_data_contract.get(agent_name):
                user_input = self._change_create_to_update_pq(agent_name, user_input)

            logging.info(f"{agent_name}'s input: {user_input}\n")

            agent_response = agent.invoke(user_input).get("data")
            logging.info(f"Agent {agent_name} result: {agent_response} / data type: {type(agent_response)}")
            results[agent_name] = self._flatten_output_data(agent_response)
        # TODO: sync data_model -> data_models (system_prompt, data type,...)
        dc_kwargs = {
            'id': 'auto-generated-id',
            'metainfo': results.get('metainfo') or current_data_contract.get('metainfo'),
            'server': results.get('server') or current_data_contract.get('server'),
            'terms': results.get('terms') or current_data_contract.get('terms'),
            'data_models': results.get('data_models') or current_data_contract.get('data_models'),
            'servicelevels': results.get('servicelevels') or current_data_contract.get('servicelevels')
        }
        try:
            state['data_contract'] = dc_kwargs
        except Exception as e:
            state['error'] = f"Error creating DataContract: {e}"
            return state
        return state

    def _create_graph(self):
        graph_builder = StateGraph(State)
        graph_builder.add_node("choose_worker_agent_node", self.choose_worker_agent_node)
        graph_builder.add_node("agent_call_node", self.agent_call_node)
        graph_builder.add_node("post_response_node", self.post_response_node)

        graph_builder.add_edge("choose_worker_agent_node", "agent_call_node")
        graph_builder.add_edge("agent_call_node", "post_response_node")
        graph_builder.add_edge("post_response_node", END)
        graph_builder.set_entry_point("choose_worker_agent_node")
        graph = graph_builder.compile()
        return graph

    def invoke(self, user_query):

        logging.info(f'current_data: {self._state['data_contract']}')

        self._state['messages'].append(HumanMessage(content=user_query))
        self._state = self._graph.invoke(self._state)
        return self._state