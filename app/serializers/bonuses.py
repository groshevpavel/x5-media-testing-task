from pydantic import BaseModel

from serializers.users import UserId


class BonusPoints(BaseModel):
    bonus_points: int


class BonusesResponse(BonusPoints, UserId):
    pass


class BonusesTransfer(BaseModel):
    recipient_id: int
    bonuses_amount: int


class BonusesTransferResponse(BaseModel):
    donor_id: int
    donor_balance: int
