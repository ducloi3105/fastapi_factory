from sqlalchemy.future import select
from src.bases.logic import Logic
from src.models import (Account)


class AccountLogic(Logic):
    def get(self, email=None):
        query = select(Account)
        if email is not None:
            query = query.where(Account.email == email)
        return query

    def create(self, email: str, name: str | None = None):
        account = Account(email=email, name=name)
        self.session.add(account)
        return account
