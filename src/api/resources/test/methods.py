from fastapi import Request, Depends
from src.bases.api.router import router
from src.bases.error.api import BadRequestParams
from fastapi import FastAPI, HTTPException

from .schemas import GetSchema

endpoint = '/test'
tags = ['test']


@router.get(endpoint, tags=tags)
async def test(payload: GetSchema = Depends(GetSchema), request: Request = None):
    return dict(success=True)
