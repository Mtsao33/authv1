import os
from typing import AsyncGenerator, Generator 

import pytest
from fastapi.testclient import TestClient # allows us to check without starting a server
from httpx import AsyncClient, ASGITransport 

os.environ["ENV_STATE"] = "test" # only if you're switching back and forth between test and prod
from database import database, user_table # noqa: E402
from main import app # noqa: E402 
# that comment calms Ruff down

transport = ASGITransport(app=app)

@pytest.fixture(scope="session") # runs once per session
def anyio_backend():
    return "asyncio" # we need async platform (asyncio framework) to run async functions on

@pytest.fixture()
def client() -> Generator: # an API
    # yield means we want to do some work before returning
    yield TestClient(app)

@pytest.fixture(autouse=True) # runs in every test, so we don't have to put db as param in every test
# async is for when this is a relational database
async def db() -> Generator:
    await database.connect() 
    yield 
    await database.disconnect() 

@pytest.fixture()
# client parameter - we don't have to pass it in explicitly which is weird! (dependency injection)
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(transport=transport, base_url = client.base_url) as ac:
        yield ac # search up async with on python

@pytest.fixture() # fixtures share data with multiple tests
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.net", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(user_table.c.email == user_details["email"])
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details

@pytest.fixture()
async def loggined_in_token(async_client: AsyncClient, registered_user: dict) -> str:
    response = await async_client.post("/token", json=registered_user)
    return response.json()["access_token"]