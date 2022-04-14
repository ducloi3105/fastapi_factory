from fastapi import Request, Depends
from src.bases.api.router import BaseRouter
from .schemas import GetSchema

endpoint = '/account'
tags = ['account']

router = BaseRouter()


@router.get(endpoint, tags=tags)
def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.session
    print(payload.search_text)
    return dict(success=True)
