from fastapi import FastAPI
import requests
from ACCESS_KEY import YOUR_API_KEY

app = FastAPI()

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
    payload = {}
    headers= {"apikey": YOUR_API_KEY}
    response = requests.get( url, headers=headers, data = payload)
    return {response.text, response.status_code}
    