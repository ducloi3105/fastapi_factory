from fastapi import Request, Depends
from src.bases.api.router import BaseRouter
from .schemas import GetSchema
arouter = BaseRouter()

endpoint = '/account'
tags = ['health-check']


@arouter.get(endpoint, tags=tags)
def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.session
    print(payload.search_text)
    return dict(success=True)
