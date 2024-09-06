import time

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()


# Define the request body model
class FibonacciRequest(BaseModel):
    number: int


# Create a ProcessPoolExecutor
executor = ProcessPoolExecutor()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/fibonacci")
async def calculate_fibonacci(request: FibonacciRequest):
    # Validate number
    number = request.number
    if number < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")

    # Record start time
    start_time = time.time()

    # Run the Fibonacci calculation in a separate process
    result = await run_fibonacci_async(number)

    # Record end time
    end_time = time.time()

    # Calculate the duration
    duration = end_time - start_time

    # Return result and execution time
    return {"result": result, "time": f"{duration:.3g}"}


def fib(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


async def run_fibonacci_async(n: int) -> int:
    loop = asyncio.get_running_loop()
    # Run the Fibonacci function in a separate process
    result = await loop.run_in_executor(executor, fib, n)
    return result
