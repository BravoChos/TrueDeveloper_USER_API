from .base_model import BaseModel

class DaysToCover(BaseModel):
    def __init__(
        self,
        security_id,
        date,
        days_to_cover_in_shares,
        short_outstanding_shares,
        twenty_days_moving_average_trading_volume,
        days_to_cover_in_amount,
        short_outstanding_amount,
        twenty_days_moving_average_trading_amount
	    ):
        vars = locals()
        self.__dict__.update(vars)
        del self.__dict__["self"]
