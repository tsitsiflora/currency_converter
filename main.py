from decimal import Decimal, getcontext
from ACCESS_KEY import YOUR_API_KEY
from fastapi import FastAPI
from schemas import Convert
import babel.numbers as bn
import requests


app = FastAPI()
headers= {"apikey": YOUR_API_KEY}


def get_rate(sender_currency: str, receiver_currency:str) -> str:
    '''This function fetches the current rates from the 
        external service.'''

    result = requests.get(
        f"https://api.apilayer.com/exchangerates_data/latest?symbols={receiver_currency}&base={sender_currency}"
        , headers=headers)
    return str(result.json().get("rates").get(receiver_currency))


def convert_amount(convert: Convert) -> Decimal:
    '''This function calculates the receiver amount, which is 
        the resulting amount by multiplying the rate 
        with the sender amount.'''

    rate = get_rate(convert.sender_currency, convert.receiver_currency)
    getcontext().prec = 4
    result_amount = Decimal(rate) * convert.sender_amount
    return result_amount


def conversion(convert: Convert) -> Convert:
    convert.receiver_amount = convert_amount(convert)
    return convert


def formatted_conversion(convert: Convert) -> Convert:
    '''This function converts the amounts into human
        readable currencies.'''

    convert.sender_amount_formatted = bn.format_currency(
        convert.sender_amount, convert.sender_currency
    )
    convert.receiver_amount_formatted = bn.format_currency(
        convert.receiver_amount, convert.receiver_currency
    )
    return convert


# defining the index endpoint decorator
@app.get("/")
async def root():
    '''This function welcomes you to the 
        currency converter API.'''
    return {"message":"Hey there, welcome to the currency convertor API."}


# defining the endpoint decorator to get all currencies
@app.get("/all")
async def get_all():
    '''This function retrieves all the currencies that the 
        currency converter is capable of supporting.'''

    url = "https://api.apilayer.com/exchangerates_data/symbols"
    response = requests.get( url, headers=headers)
    return {response.text, response.status_code}


# defining the endpoint decorator to convert from one 
# currency to another
@app.post("/convert", response_model=Convert)
async def convert_currency(convert: Convert):
    return formatted_conversion(convert_amount(convert))