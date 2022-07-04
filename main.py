from fastapi import FastAPI

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
    