from fastapi import Request
from src.bases.api.router import BaseRouter

router = BaseRouter()

endpoint = '/health-check'
tags = ['health-check']


@router.get(endpoint, tags=tags)
def health_check(request: Request):
    session = request.state.session
    return dict(success=True)
