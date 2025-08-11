"""
This module defines a simple FastAPI application that includes a root endpoint,
an echo endpoint, and a demo endpoint for greeting users and calculating squares.
"""

from typing import Annotated
from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class Echo(BaseModel):
    """Pydantic model used as the request body for the /echo endpoint.

    Attributes:
        text: The string to echo back to the caller.
    """

    text: str

    def length(self) -> int:
        """Return length of the given input"""
        return len(self.text)

    def to_dict(self) -> dict:
        """Return the model as a plain dictionary."""
        return self.dict()

    def shout(self) -> str:
        """Return the text in uppercase (convenience helper)."""
        return self.text.upper()


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
    return {"echo": payload.shout(), "echo_length": payload.length()}


@app.get("/greet/{name}", tags=["demo"])
def greet(name: str = Path(..., min_length=1, max_length=50)):
    """greet the api user"""
    return {"message": f"Hello {name}!!!"}


@app.get("/math/square", tags=["demo"])
def square(x: int = Query(..., ge=-1_000_000, le=1_000_000)):
    """return square input"""
    return {"x": x, "square": x * x}


# ----- simple in-memory users with validation -----


class UserIn(BaseModel):
    """
    User input model for user creation or update.
    """

    name: str = Field(min_length=1, max_length=80, examples=["Pandi"])
    email: EmailStr = Field(examples=["pandi@example.com"])

    age: Annotated[int, Field(ge=0, le=120)] = 30  # constrained int with defaults

    # Controls schema/docs behavior (and other model config)
    model_config = ConfigDict(
        json_schema_extra={"example": {"name": "Pandi", "email": "pandi@example.com", "age": 30}},
        # Consider forbidding extra fields to make contracts strict:
        # extra="forbid",
    )


class UserOut(BaseModel):
    """
    Output model for user data returned by the API.
    """

    id: int
    name: str
    email: EmailStr

    def display_name(self) -> str:
        """Return a formatted display name for the user."""
        return f"{self.name} <{self.email}>"

    def to_dict(self) -> dict:
        """Return the user data as a dictionary."""
        return self.dict()


_USERS: dict[int, dict] = {}
_STATE = {"next_id": 1}


@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: UserIn):
    """
    Creates a new user and adds them to the in-memory user store.

    Performs a case-insensitive check to ensure the email does not already exist.
    If the email is already registered, raises an HTTP 409 Conflict error.
    """
    # basic duplicate check
    if any(u["email"].lower() == user.email.lower() for u in _USERS.values()):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    uid = _STATE["next_id"]
    _STATE["next_id"] += 1
    payload = {"id": uid, **user.model_dump()}
    _USERS[uid] = payload
    return payload


@app.get("/users/{user_id}", response_model=UserOut, tags=["users"])
def get_user(
    user_id: Annotated[int, Path(..., ge=1, description="The ID of the user to retrieve")]
):
    """
    Retrieve a user by their user_id from the in-memory user store.
    Returns 404 if the user does not exist.
    """
    user = _USERS.get(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(**user)
