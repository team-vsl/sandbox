from langgraph.graph import START, END
from typing import Dict
from genai.models import DefinitionObject
from pydantic import BaseModel
from .base_sub_agent import BaseSubAgent, SubState
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser


class FieldDefinitions(BaseModel):
    definitions: Dict[str, DefinitionObject]


class DefinitionsAgent(BaseSubAgent):
    def __init__(self, llm_instance):
        super().__init__(llm_instance)

    def _load_system_prompt(self):
        with open("/var/vpbank/datacontracts/sandbox/data/system_prompt/definitions.txt", "r", encoding="utf-8") as fp:
            data = fp.read()
        return {"create_object": data}
    
    def create_object_node(self, state: SubState):
        system_prompt = self._system_prompt.get("create_object")
        parser = JsonOutputParser(pydantic_object=FieldDefinitions)

        human_request = state.get("messages")[-1]

        if not isinstance(human_request, HumanMessage):
            return state
        
        messages = [SystemMessage(content=system_prompt), human_request]

        response = self._llm.invoke(messages)
        state["data"] = parser.parse(response.content)
        return state
    


