from typing import List, Dict
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.output_parsers import CommaSeparatedListOutputParser, JsonOutputParser
from typing import TypedDict, Annotated, Union
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, SystemMessage
from genai.models import Server, S3Server, RedshiftServer
import os
import time


class ServerAgentState(TypedDict):
    messages: Annotated[List, add_messages]
    data: Union[Server, None]
    server_type: List
    error: str
    sys_prompt: Dict


class RedShiftServerField(BaseModel):
    server: Dict[str, RedshiftServer]


class S3ServerField(BaseModel):
    server: Dict[str, S3Server]


class ServerAgent:
    def __init__(self, llm_instance):
        self._graph = self._create_graph()
        self._llm = llm_instance
        
    def detect_type(self, user_input: HumanMessage) -> str:
        classification_prompt = """
 You are a system that classifies which server system can be used to store data. Server can be database, data lake, or data warehouse services.

Supported server types:
- "s3": aws s3 server
- "redshift": aws redshift server
- "gcs": google cloud storage
- "glue": aws glue

Based on the user's input, return the server(s) that are suitable: "s3", "redshift", "gcs", "glue".

- You can return multiple server types, separated by commas.
- If no server is suitable, return exactly: "invalid"
- Output format: a plain list of server names, separated by commas.
- Do not return brackets, quotes, sets, dictionaries, or any explanation.

Example:
User_input: I need use s3 & redshift for data warehouse  
Output: s3, redshift
        """

        message = [
            SystemMessage(content=classification_prompt),
            user_input
        ]


        response = self._llm.invoke(message)

        time.sleep(60)

        return response
    
    def check_type_node(self, state: ServerAgentState) -> ServerAgentState:
        input_text = state.get("messages")[-1]

        if not isinstance(input_text, HumanMessage):
            return state

        allowed_types = ["redshift", "s3"]
        response = self.detect_type(input_text)

        parser = CommaSeparatedListOutputParser()
        detected_type = parser.parse(response.content)

        for item in detected_type:
            if item not in allowed_types:
                state['error'] = "Error with detect type: {detected_type}".format(detected_type=detected_type)
                return state

        state['server_type'] = detected_type
        return state

    def load_system_prompt(self, state: ServerAgentState) -> ServerAgentState:
        
        server_types = state.get("server_type")

        system_prompt = {}

        for type in server_types:
            path = f"/var/vpbank/datacontracts/sandbox/data/system_prompt/{type}_server.txt"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as fp: 
                    prompt = fp.read()
                system_prompt[type] = prompt
            else:
                system_prompt[type] = None
                
        state["sys_prompt"] = system_prompt

        return state

    def generate_object_node(self, state: ServerAgentState) -> ServerAgentState:
        
        object_dict = {"redshift": RedShiftServerField, "s3": S3ServerField}
        sys_prompt_list = state.get("sys_prompt")

        human_request = state.get("messages")[-1]

        all_servers = {}

        if not isinstance(human_request, HumanMessage):
            return state

        for key, sys_prompt in sys_prompt_list.items():

            if not sys_prompt:
                continue
            
            messages = [SystemMessage(content=sys_prompt), human_request]
            parser = JsonOutputParser(pydantic_object=object_dict[key])

            response = self._llm.invoke(messages)
            all_servers.update(parser.parse(response.content))

            time.sleep(60)

        state["data"] = all_servers
        return state

    @staticmethod
    def should_continue(state: ServerAgentState):
        if state.get("error") is not None:
            return "end"
        else:
            return "continue"
    
    def _create_graph(self):
        graph_builder = StateGraph(ServerAgentState)
        graph_builder.add_node("check_type", self.check_type_node)
        graph_builder.add_node("load_prompt", self.load_system_prompt)
        graph_builder.add_node("generate_data", self.generate_object_node)

        graph_builder.add_conditional_edges("check_type", self.should_continue, {"continue": "load_prompt", "end": END})
        graph_builder.add_edge("load_prompt", "generate_data")
        graph_builder.add_edge("generate_data", END)

        graph_builder.set_entry_point("check_type")

        graph = graph_builder.compile()
        return graph
    
    def invoke(self, user_query):
        state = ServerAgentState(messages=[HumanMessage(content=user_query)])
        rs = self._graph.invoke(state)
        return rs