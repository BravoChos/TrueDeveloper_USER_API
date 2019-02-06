from .base_model import BaseModel

class PremiumUser(BaseModel):
    def __init__(
        self,
        username,
        hashed_password,
        account_level_id,
        created_at,
        updated_at
        ):
        vars = locals()
        self.__dict__.update(vars)
        del self.__dict__["self"]
