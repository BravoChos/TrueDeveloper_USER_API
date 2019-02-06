from .base_model import BaseModel

class ShortVolumePercentage(BaseModel):
    def __init__(
        self,
        security_id,
        date,
        short_volume_percentage,
        short_volume,
        trading_volume
        ):
        vars = locals()
        self.__dict__.update(vars)
        del self.__dict__["self"]
