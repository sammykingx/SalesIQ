from dataclasses import dataclass
from pydantic import EmailStr, UUID7
from typing import Union


@dataclass
class UserEntity:
    id: UUID7
    first_name: str
    last_name: str
    email: EmailStr
    mobile_number: Union[str, None]
    is_verified: bool
    