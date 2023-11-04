import json
from typing import Any, Dict, Union, List, TYPE_CHECKING
from pydantic import BaseModel
from pathlib import Path

from nonebot.adapters.red.api.model import Element


def process_message(elements: List[Element]) -> str:
    result = ""
    for element in elements:
        if element.elementType == 1:
            if TYPE_CHECKING:
                assert element.textElement
            text = element.textElement
            if not text.atType:
                result += text.content
            elif text.atType == 1:
                result += "@全体成员 "
            elif text.atType == 2:
                result += f"{text.content} "
        if element.elementType == 2:
            result += "[图片]"
        if element.elementType == 3:
            result += "[文件]"
        if element.elementType == 4:
            result += "[语音]"
        if element.elementType == 5:
            result += "[视频]"
        if element.elementType == 6:
            result += "[动画表情]"
        if element.elementType == 7:
            result += "[回复]"
        if element.elementType == 10:
            result += "[小程序]"
        if element.elementType == 11:
            if TYPE_CHECKING:
                assert element.marketFaceElement
            market_face = element.marketFaceElement
            result += f"[{market_face.faceName}]"
        if element.elementType == 16:
            result += "[合并转发]"

    return result


class JsonDataStorage:
    """基于 Pydantic 的 JSON 数据读写方法"""

    def __init__(
        self,
        model: Union[BaseModel, List[BaseModel]] = None,
        file_path: Union[str, Path] = "",
    ):
        """基于 Pydantic 的 JSON 数据读写方法

        参数:
        - model (Union[BaseModel, List[BaseModel]], optional): 父类为 BaseModel 的模型
        - file_path (Union[str, Path]): 要保存数据的文件路径
        """
        if not file_path:
            raise ValueError("File path is required.")
        self.model = model
        self.file_path = file_path

    def load(self) -> "JsonDataStorage.model":
        """
        从指定的文件路径加载 JSON 数据并将其转换为模型对象

        返回:
        - BaseModel: 解析后的模型对象
        """
        return self.model.parse_file(self.file_path)

    def load_as_list(self) -> List["JsonDataStorage.model"]:
        """
        从指定的文件路径加载 JSON 数据并将其转换为模型对象列表

        返回:
        - List[BaseModel]: 解析后的模型对象列表
        """
        with open(self.file_path, "r", encoding="UTF-8") as file:
            data: List[Dict[Any, Any]] = json.load(file)
        return [self.model.parse_obj(d) for d in data]

    def save(self, data: BaseModel) -> None:
        """
        将模型对象转换为 JSON 数据并保存到指定的文件路径

        参数:
        - data (BaseModel): 要保存的模型对象
        """
        with open(self.file_path, "w", encoding="UTF-8") as file:
            json.dump(data.dict(), file, indent=4)

    def save_as_list(self, data: List[BaseModel]) -> None:
        """
        将模型对象转换为列表 JSON 数据并保存到指定的文件路径

        参数:
        - data (List[BaseModel]): 要保存的模型对象列表
        """
        if type(data) != list:
            raise ValueError("Only list-like object is suitable for this method.")
        with open(self.file_path, "w", encoding="UTF-8") as file:
            json.dump([d.dict() for d in data], file, indent=4)
