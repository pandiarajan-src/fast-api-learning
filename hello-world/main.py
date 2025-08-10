"""
Simple hello world application
"""

from fastapi import FastAPI
from pydantic import BaseModel


class Echo(BaseModel):
    text: str


# Create FastAPI app instance
app = FastAPI()


# Define a Get Endpoint
@app.get("/")
def read_root():
    """root response"""
    return {"message": "Hello FastAPI!!!"}


@app.post("/echo")
def echo(payload: Echo):
    """echo api endpoint"""
    return {"echo": payload.text}
