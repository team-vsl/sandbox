import json
from pathlib import Path
from abc import ABC, abstractmethod
from langchain_core.messages import BaseMessage
from typing import Any, Dict, Type, get_origin, get_args, List, Union
from pydantic import BaseModel, ValidationError


class BaseSubAgent(ABC):
    def __init__(self, llm_instance):
        self._graph = self._create_graph()
        self._llm = llm_instance
        self._system_prompt: Dict[str, str] = self._get_sys_prompt()
        self._state = self._get_state()

    @abstractmethod
    def _get_state(self):
        pass

    @abstractmethod
    def _create_graph(self):
        pass

    @abstractmethod
    def _get_sys_prompt_path(self) -> Path:
        pass

    def _get_sys_prompt(self) -> Dict[str, str]:
        sys_prompt_path = self._get_sys_prompt_path()   

        try:
            with open(sys_prompt_path, "r", encoding="utf-8") as fp:
                sys_prompt = json.load(fp)
        except Exception as e:
            sys_prompt = {}
            print(f"Warning: Cannot read JSON file {sys_prompt_path}: {e}")
        return sys_prompt

    def invoke(self, messages: List[BaseMessage]):
        self._state.get('messages').extend(messages)
        rs = self._graph.invoke(self._state)
        return rs

    @staticmethod
    def normalize_and_validate(model_cls: Type[BaseModel], data: Dict[str, Any]) -> BaseModel:
        """
        Chuẩn hóa và validate dữ liệu theo model_cls, hỗ trợ nested, List, Union (discriminator).
        """
        normalized_data = {}

        for field_name, field_info in model_cls.model_fields.items():
            if field_name in data and data[field_name] is not None:
                value = data[field_name]
                annotation = field_info.annotation
                origin = get_origin(annotation)

                # Xử lý List
                if origin is list or origin is List:
                    item_type = get_args(annotation)[0]  # Kiểu phần tử
                    normalized_list = []

                    if isinstance(value, list):
                        for item in value:
                            # Nếu là BaseModel → đệ quy
                            if hasattr(item_type, "model_fields"):
                                if isinstance(item, dict):
                                    normalized_list.append(__class__.normalize_and_validate(item_type, item))
                                elif isinstance(item, item_type):
                                    normalized_list.append(item)
                            # Nếu là Union → xác định model con theo discriminator
                            elif get_origin(item_type) is Union:
                                sub_models = get_args(item_type)
                                if isinstance(item, dict) and "type" in item:
                                    matched_model = next((m for m in sub_models if hasattr(m, "__fields__") and getattr(m, "__name__", "") == item["type"].capitalize()+"Check"), None)
                                    if matched_model:
                                        normalized_list.append(__class__.normalize_and_validate(matched_model, item))
                                    else:
                                        normalized_list.append(item)
                                else:
                                    normalized_list.append(item)
                            else:
                                normalized_list.append(item)
                    normalized_data[field_name] = normalized_list

                # Nếu là nested BaseModel
                elif hasattr(annotation, "model_fields"):
                    if isinstance(value, dict):
                        normalized_data[field_name] = __class__.normalize_and_validate(annotation, value)
                    elif isinstance(value, annotation):
                        normalized_data[field_name] = value
                    else:
                        normalized_data[field_name] = None
                else:
                    normalized_data[field_name] = value
            else:
                # Field bị thiếu
                if field_info.annotation == str:
                    normalized_data[field_name] = ""
                else:
                    normalized_data[field_name] = None

        try:
            return model_cls(**normalized_data)
        except ValidationError as e:
            print(f"Validation error in {model_cls.__name__}: {e}")
            return model_cls(**{k: None if v != "" else "" for k, v in normalized_data.items()})
