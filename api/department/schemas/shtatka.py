from pydantic import BaseModel
from typing import List


class ChangeShtatkaStatus(BaseModel):
    status: str
    client_shtatka_id: int
