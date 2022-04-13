from fastapi import APIRouter


class BaseRouter(APIRouter):

    def __init__(self, *args, **kwargs):
        APIRouter.__init__(self)
