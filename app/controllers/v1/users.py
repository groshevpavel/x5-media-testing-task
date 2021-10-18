from asyncpg.exceptions import UniqueViolationError
from db import database
from fastapi import (
    APIRouter,
    HTTPException,
)
from models.bonuses import bonuses
from models.users import users
from serializers.users import (
    UserAdd,
    UserAdded,
)
from starlette import status

v1_users = APIRouter()


@v1_users.post('/users/add', response_model=UserAdded)
async def add_user(user_add: UserAdd):
    query = users.insert().values(firstname=user_add.firstname, lastname=user_add.lastname)
    try:
        user_id = await database.execute(query)
    except UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists',
        )

    query = bonuses.insert().values(userid=user_id, points=user_add.bonus_points)
    await database.execute(query)

    return {
        'firstname': user_add.firstname, 'lastname': user_add.lastname,
        'bonus_points': user_add.bonus_points, 'id': user_id,
    }


@v1_users.get('/users/{user_id}', response_model=UserAdded)
async def user_info(user_id: int):
    query = """SELECT u.id, u.firstname, u.lastname, b.points as bonus_points
    FROM users u JOIN bonuses b ON u.id=b.userid 
    WHERE u.id = :user_id"""

    result = await database.fetch_one(query=query, values={'user_id': user_id})

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID#{user_id} does not exists',
        )

    return result
