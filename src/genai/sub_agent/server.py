from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import CommaSeparatedListOutputParser, JsonOutputParser
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from genai.models import S3Server, RedshiftServer, DataServer
import time
from pathlib import Path
from genai.sub_agent.base_sub_agent import BaseSubAgent


class ServerAgentState(TypedDict):
    messages: Annotated[List, add_messages]
    data: DataServer
    server_type: List


class ServerAgent(BaseSubAgent):
    def __init__(self, llm_instance):
        super().__init__(llm_instance=llm_instance)

    def _get_state(self):
        return ServerAgentState(messages=[], data=None, server_type=[])

    def _get_sys_prompt_path(self) -> Path:
        base_path = Path(__file__).parent.parent.parent.parent / "data" / "system_prompt"
        return base_path / "server.json"

    def _create_default_model(self) -> DataServer:
        """Create a default DataServer object with empty values."""
        return DataServer(server={
            "default_s3_servers": {
                "type": "s3",
                "definitions": None,
                "environment": "dev",
                "roles": None
            }
        })
        
    def detect_type(self, user_input: List[HumanMessage]) -> str:
        classification_prompt = self._system_prompt["server_classifier_instruction"]
        if not classification_prompt:
            raise ValueError("Classification prompt not found")
        
        message = [
            SystemMessage(content=classification_prompt)
        ] + user_input
        print("\n", message, "\n")

        response = self._llm.invoke(message)
        time.sleep(30)

        return response
    
    def check_type_node(self, state: ServerAgentState) -> ServerAgentState:
        input_text = [request for request in state.get("messages") if isinstance(request, HumanMessage)]

        allowed_types = ["redshift", "s3"]
        response = self.detect_type(input_text)

        parser = CommaSeparatedListOutputParser()
        print("\n" + response.content + "\n")
        if len(response.content.split()) > 4:
            state['server_type'] = []
            return state

        detected_type = parser.parse(response.content)

        for item in detected_type:
            if item not in allowed_types:
                print("Error with detect type: {detected_type}".format(detected_type=detected_type))
                continue

        state['server_type'] = detected_type
        return state

    def generate_object_node(self, state: ServerAgentState) -> ServerAgentState:
        if not state['server_type']:
            state['data'] = self._create_default_model()
            return state

        object_dict = {"redshift": RedshiftServer, "s3": S3Server}
        sys_prompt_list = self._system_prompt
        server_types = state.get("server_type")
        all_servers = {}
                
        human_requests = [request for request in state.get("messages") if isinstance(request, HumanMessage)]

        for server_type in server_types:
            sys_prompt = sys_prompt_list.get(server_type + "_create_object")
            if not sys_prompt:
                continue

            messages = [SystemMessage(content=sys_prompt)] + human_requests
            parser = JsonOutputParser(pydantic_object=object_dict[server_type])
            max_retries = 3

            #TODO: The is bug with s3_server, which return all field not only the server fields.

            for attempt in range(max_retries):
                response = self._llm.invoke(messages)
                time.sleep(30)
                try:
                    draw_data = parser.parse(response.content).get("server", {})

                    print("draw_data:\n", draw_data,"\n")

                    #TODO: Fast way to demo, need better validate in future (except_data_model_class=DataServer)
                    data = super().normalize_and_validate(DataServer, {"server": draw_data})
                    if data:
                        all_servers[server_type] = data
                        break
                except Exception as e:
                    print(e)
                    if attempt == max_retries - 1:
                        state['data'] = self._create_default_model()
                        return state
        state["data"] = all_servers
        return state

    @staticmethod
    def should_continue(state: ServerAgentState):
        if state.get("server_type") is None:
            return "end"
        else:
            return "continue"
    
    def _create_graph(self):
        graph_builder = StateGraph(ServerAgentState)
        graph_builder.add_node("check_type", self.check_type_node)
        graph_builder.add_node("generate_data", self.generate_object_node)

        graph_builder.add_conditional_edges("check_type", self.should_continue, {"continue": "generate_data", "end": END})
        graph_builder.add_edge("generate_data", END)
        graph_builder.set_entry_point("check_type")

        graph = graph_builder.compile()
        return graph