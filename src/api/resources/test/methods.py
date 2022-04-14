from fastapi import Request, Depends
from src.bases.api.router import BaseRouter
from src.bases.error.api import BadRequestParams

from .schemas import GetSchema

endpoint = '/test'
tags = ['test']

router = BaseRouter()


@router.get(endpoint, tags=tags)
def test(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.session
    print(payload.search_text)
    return dict(success=True)
