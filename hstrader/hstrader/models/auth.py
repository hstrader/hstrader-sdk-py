from .base import BaseModel
from typing import Union


class AuthResponse(BaseModel):

    account_id: Union[int, None]
    access_token: Union[str, None]
    refresh_token: Union[str, None]
    session_id: Union[str, None]
    expires_in: Union[int, None]
    ip_address: Union[str, None]
    scope: Union[str, None]
