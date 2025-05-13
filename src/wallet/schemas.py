import uuid
from pydantic import BaseModel


class WalletAddModel(BaseModel):
    credit: float


class WalletGetModel(WalletAddModel):
    uid: uuid.UUID
