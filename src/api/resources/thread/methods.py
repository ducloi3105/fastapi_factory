from fastapi import Request, Depends
from fastapi import FastAPI, HTTPException

from src.bases.api.router import router
from src.bases.error.api import BadRequestParams
from src.logic.postgres.thread import ThreadLogic
from src.common.utils import paginate
from .schemas import GetSchema

endpoint = '/thread'
tags = ['thread']


@router.get(endpoint, tags=tags)
def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.session
    folder = payload.folder
    thread_logic = ThreadLogic(session)
    query = thread_logic.find_thread(folder)
    threads = []
    for thread in paginate(query, payload.page, payload.per_page):
        threads.append(thread.to_json())
    return dict(success=True, threads=threads)
