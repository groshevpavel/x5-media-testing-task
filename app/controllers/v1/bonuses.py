from db import database
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
)
from starlette import status

from serializers.bonuses import BonusesResponse, BonusesTransfer, BonusesTransferResponse

v1_bonuses = APIRouter()


@v1_bonuses.put('/users/{user_id}/bonuses/{bonus_points}', response_model=BonusesResponse)
async def set_user_bonuses(user_id: int, bonus_points: int = Path(..., ge=0, le=10000)):
    query = """INSERT into bonuses (userid, points)
    SELECT :user_id, :bonus_points
    WHERE EXISTS (
        select 1 FROM bonuses b WHERE b.userid = :user_id
    )
    RETURNING id;
    """

    result = await database.execute(query=query, values={'user_id': user_id, 'bonus_points': bonus_points})

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID#{user_id} does not exists',
        )

    return {'id': user_id, 'bonus_points': bonus_points}


@v1_bonuses.delete('/users/{user_id}/bonuses/{write_off_points}', response_model=BonusesResponse)
async def write_off_user_bonuses(user_id: int, write_off_points: int = Path(..., ge=0, le=10000)):
    query = """UPDATE bonuses SET points = (CASE 
        WHEN points - :write_off_points >= 0
        THEN points - :write_off_points
        ELSE 0 END)
    WHERE bonuses.id = (SELECT b.id FROM bonuses b WHERE b.userid = :user_id ORDER BY b.id DESC LIMIT 1)
    RETURNING points;
    """

    updated_points = await database.execute(
        query=query, values={'user_id': user_id, 'write_off_points': write_off_points})

    if updated_points is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID#{user_id} does not exists',
        )

    return {'id': user_id, 'bonus_points': updated_points}


@v1_bonuses.post('/users/{donor_user_id}/bonuses/transfer', response_model=BonusesTransferResponse)
async def transfer_user_bonuses(donor_user_id: int, transfer: BonusesTransfer):
    query = """UPDATE bonuses SET points = tt.points
    FROM (VALUES
        (
            (SELECT b.id FROM bonuses b WHERE b.userid = :donor_user_id ORDER BY b.id DESC LIMIT 1),
            (SELECT CASE WHEN b.points - :transfer_points >= 0 THEN b.points - :transfer_points ELSE b.points END 
                FROM bonuses b WHERE b.userid = :donor_user_id ORDER BY b.id DESC LIMIT 1)
        ),
        (
            (SELECT b.id FROM bonuses b WHERE b.userid = :recipient_user_id ORDER BY b.id DESC LIMIT 1),
            (SELECT CASE WHEN 
                (SELECT bdonor.points 
                    FROM bonuses bdonor 
                    WHERE bdonor.userid = :donor_user_id
                    ORDER BY b.id DESC LIMIT 1) - :transfer_points >= 0 
                THEN b.points + :transfer_points ELSE b.points END 
                FROM bonuses b WHERE b.userid = :recipient_user_id ORDER BY b.id DESC LIMIT 1)
        )
    ) as tt (id, points)
    WHERE bonuses.id = tt.id
    RETURNING bonuses.points;"""

    donor_points = await database.execute(
        query=query,
        values={
            'donor_user_id': donor_user_id,
            'recipient_user_id': transfer.recipient_id,
            'transfer_points': transfer.bonuses_amount,
        },
    )

    return {
        'donor_id': donor_user_id, 'donor_balance': donor_points,
    }


@v1_bonuses.get('/users/{user_id}/bonuses', response_model=BonusesResponse)
async def get_user_bonuses(user_id: int):
    query = """SELECT b.userid as id, b.points as bonus_points 
    FROM bonuses b
    WHERE b.userid = :user_id
    ORDER BY b.timestamp DESC
    LIMIT 1"""

    result = await database.fetch_one(query=query, values={'user_id': user_id})

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID#{user_id} does not exists',
        )

    return result
