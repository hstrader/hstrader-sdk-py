from .base import BaseModel
from typing import Union,List


class BaseResponse(BaseModel):
    success: bool
    code: int
    data: Union[dict, None, str, int, float, bool, list]
    error: str
    message: str

    def deserialize(self, cls: BaseModel) -> BaseModel:
        if self.data is not None:
            if isinstance(self.data, list):
                raise ValueError("deserialize should be used only single object data")
            return cls(**self.data)

    def deserialize_list(self, cls: BaseModel) -> List[BaseModel]:
        if self.data is not None:
            if not isinstance(self.data, list):
                raise ValueError("deserialize_list should be used only with list data")
            return [cls(**item) for item in self.data]

