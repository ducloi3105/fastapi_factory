from fastapi import Request, Depends
from fastapi import FastAPI, HTTPException

from src.bases.api.router import router
from src.bases.error.api import BadRequestParams
from src.logic.postgres.thread import ThreadLogic
from src.common.utils import paginate
from .schemas import GetSchema

endpoint = '/thread_async'
tags = ['thread']


@router.get(endpoint, tags=tags)
async def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.async_session
    thread_logic = ThreadLogic(session)
    import time
    x = time.time()
    query = thread_logic.find_thread2(folder=payload.folder)
    query = await session.execute(
        query
    )
    thread = query.fetchone()
    return dict(success=True)
