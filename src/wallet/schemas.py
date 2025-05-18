import uuid
from pydantic import BaseModel


class WalletAddModel(BaseModel):
    credit: float


class WalletGetModel(BaseModel):
    uid: uuid.UUID
    customer_uid: uuid.UUID
    credit: float
