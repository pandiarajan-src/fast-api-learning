"""Main module for FastAPI application."""

import asyncio

from fastapi import FastAPI

app = FastAPI(title="Hello FastAPI", version="1.0.0")


@app.get("/health")
async def health_check():
    """Endpoint to check the health status of the application."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint returning a welcome message."""
    return {"message": "Hello World"}


@app.get("/echo")
async def echo(message: str | None = None):
    """Echo back the received message."""
    return {"message": message}


@app.get("/greet/{name}")
async def greet(name: str, excited: bool = False):
    """Greet a user by name."""
    msg = f"Hello, {name}"
    if excited:
        msg += "!!!"
    # time.sleep(20)
    await asyncio.sleep(20)
    return {"greeting": msg}
