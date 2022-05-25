import time
from fastapi import Request, Depends
from fastapi import FastAPI, HTTPException

from src.bases.api.router import router
from src.bases.error.api import BadRequestParams
from src.logic.postgres.thread import ThreadLogic, Folder
from src.common.utils import paginate
from .schemas import GetSchema

endpoint = '/thread'
tags = ['thread']


@router.get(endpoint, tags=tags)
def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.session
    folder = payload.folder
    folder = session.query(Folder).filter(
        Folder.name == folder
    ).first()
    thread_logic = ThreadLogic(session)
    query = thread_logic.find_thread(folder.name)
    # threads = []
    # for thread in paginate(query, payload.page, payload.per_page):
    #     threads.append(thread.to_json())
    t = time.time()
    t1 = query.count()
    print('count 1', t1, time.time() - t)

    x = time.time()
    query2 = thread_logic.find_thread3(folder.id)
    t2 = query2.count()
    print('count 2', t2, time.time() - x)
    return dict(success=True, threads=[])
