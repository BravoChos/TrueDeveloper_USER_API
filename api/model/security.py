from .base_model import BaseModel

class Security(BaseModel):
    def __init__(
        self,
        id,
        ticker,
        name,
        english_name
        ):
        vars = locals()
        self.__dict__.update(vars)
        del self.__dict__["self"]
