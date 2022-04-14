from sqlalchemy.future import select
from src.bases.logic import Logic
from src.bases.error.core import CoreError
from src.models import (Account)


class AccountLogic(Logic):
    def get(self, email=None):
        query = select(Account)
