from .base_model import BaseModel

class LoanOutstandingPercentage(BaseModel):
    def __init__(
        self,
        security_id,
        date,
        loan_utilization_percentage,
        loan_outstanding_shares,
        floating_shares,
        loan_utilization_percentage_shares,
        loan_utilization_percentage_amount,
        all_outstanding_shares,
        prev_valid_free_floats,
        prev_valid_outstanding_shares,
        market_cap,
        loan_outstanding_amount
        ):         
        vars = locals() 
        self.__dict__.update(vars)
        del self.__dict__["self"]		