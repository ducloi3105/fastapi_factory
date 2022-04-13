from fastapi import Request
from src.bases.api.router import BaseRouter
from src.bases.error.api import BadRequestParams

from .schemas import GetSchema

router = BaseRouter()

endpoint = '/health-check'
tags = ['health-check']


@router.post(endpoint, tags=tags)
def test(payload: GetSchema, request: Request):
    session = request.state.session
    return dict(success=True)
