from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Define the request body model
class FibonacciRequest(BaseModel):
    number: int


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/fibonacci")
async def calculate_fibonacci(request: FibonacciRequest):

    print("lol")
    # Validate number
    number = request.number
    if number < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")

    # Calculate fibonacci
    result = fib(number)

    # Return result
    return {"result": result}


def fib(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)
