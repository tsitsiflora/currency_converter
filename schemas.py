from decimal import Decimal
from typing import Optional

import babel.numbers as bn
from pydantic import BaseModel, validator,UUID4


CURRENCIES = bn.list_currencies()
CURRENCY_VALUE_ERROR = ValueError(
    "Invalid currency code submitted. "
    f"Value must be one of the following {', '.join(CURRENCIES)}.")


class Convert(BaseModel):
    sender_currency: str
    sender_amount: Decimal
    sender_amount_formatted: Optional[str]
    receiver_currency: str
    receiver_amount_formatted: Optional[str]
    receiver_amount: Optional[Decimal]

    @validator('sender_amount')
    def positive_sender_amount(cls: BaseModel, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError('Amount must be a positive number.')
        return v

    @validator('receiver_amount')
    def positive_receiver_amount(cls: BaseModel, v: Decimal) -> Decimal:
        if v and v <= 0:
            raise ValueError('Amount must be a positive number.')
        return v

    @validator('receiver_currency')
    def valid_receiver_currency(cls: BaseModel, v: str) -> str:
        if v not in CURRENCIES:
            raise CURRENCY_VALUE_ERROR
        return v

    @validator('sender_currency')
    def valid_sender_currency(cls: BaseModel, v: str) -> str:
        if v not in CURRENCIES:
            raise CURRENCY_VALUE_ERROR
        return v