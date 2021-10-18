from fastapi import FastAPI

from controllers.v1.users import v1_users
from controllers.v1.bonuses import v1_bonuses
from db import database

app = FastAPI()

app.include_router(v1_users, prefix='/v1', tags=['v1'])
app.include_router(v1_bonuses, prefix='/v1', tags=['v1'])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
