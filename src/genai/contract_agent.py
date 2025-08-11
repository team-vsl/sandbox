from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import CommaSeparatedListOutputParser, StrOutputParser
from typing import TypedDict, Annotated, Dict
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from . import sub_agent
import time
from pathlib import Path
from .root_model import DataContract
from langgraph.checkpoint.memory import InMemorySaver
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
    def __init__(self, llm_instance):
        self._llm = llm_instance
        self._memory = InMemorySaver()
        self._worker_agents = self._init_worker_agents()
        self._sys_prompt = self._get_sys_prompt()
        self._graph = self._create_graph()
        self._state = State(messages=[], worker_agent=[], data_contract=None, check_intent_message="", error="")
        

    def _create_default_model(self) -> DataContract:
        """Create a default DataServer object with empty values."""
        return DataContract(
            id="",
            metainfo=None,
            servers=None,
            models=None,
            terms=None,
            servicelevels=None
        )

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
        # Ánh xạ tên worker_agent sang class agent tương ứng
        return {
            "meta_info": sub_agent.InfoAgent(self._llm),
            "data_model": sub_agent.DataModelAgent(self._llm),
            "server": sub_agent.ServerAgent(self._llm),
            "servicelevels": sub_agent.ServiceLevelsAgent(self._llm),
            "terms": sub_agent.TermsAgent(self._llm),
        }

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

        post_response_prompt = self._sys_prompt["check_required_info"]
        logging.info("Post response processing")

        messages = [
            SystemMessage(content=post_response_prompt), *user_inputs
        ]

        response = self._llm.invoke(messages)
        time.sleep(20)

        state['messages'].append(AIMessage(content=response.content))

        return state

    def choose_worker_agent_node(self, state: State) -> State:
        messages = state.get("messages", [])
        # Lấy 3 message gần nhất
        user_inputs = [msg for msg in messages if isinstance(msg, HumanMessage)][-3:]
        if not user_inputs:
            return state
        worker_agent_posible = ["data_model", "metainfo", "server", "servicelevels", "terms"]
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
        worker_agents = state.get("worker_agent", [])
        results = {}
        for agent_name in worker_agents:
            agent = self._worker_agents.get(agent_name)
            if agent is None:
                state['error'] = f"Không tìm thấy agent cho worker_agent: {agent_name}"
                continue

            logging.info(f"Agent {agent_name} running")

            agent_result = agent.invoke(user_input)

            logging.info(f"Agent {agent_name} result: {agent_result.get('data')}")

            # Lấy trường data từ kết quả trả về
            if hasattr(agent_result, 'get'):
                data = agent_result.get('data', agent_result)
            else:
                data = agent_result
            results[agent_name] = data

        dc_kwargs = {
            'id': 'auto-generated-id',
            'info': results.get('metainfo') or {},
            'server': results.get('server') or {},
            'terms': results.get('terms') or {},
            'data_models': results.get('data_model') or {},
            'servicelevels': results.get('servicelevels') or {}
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
        self._state['messages'].append(HumanMessage(content=user_query))
        rs = self._graph.invoke(self._state)
        return rs