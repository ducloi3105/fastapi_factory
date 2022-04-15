from src.bases.api import Request
from src.bases.api.router import router

endpoint = '/health-check'
tags = ['health-check']


@router.get(endpoint, tags=tags)
def health_check(request: Request):
    return dict(success=True)
