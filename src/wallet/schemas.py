import uuid
from pydantic import BaseModel


class WalletAddModel(BaseModel):
    customer_uid: uuid.UUID
    credit: float
    
    def __iadd__(self, amount: float):
        if not isinstance(amount, (int, float)):
            raise TypeError("Can only add a number to Wallet")
        self.credits += amount
        return self

class WalletGetModel(WalletAddModel):
    pass
