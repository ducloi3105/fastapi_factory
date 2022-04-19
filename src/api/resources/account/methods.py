from src.bases.api import Request, Depends
from src.bases.api.router import router
from src.logic.postgres.account import AccountLogic
from src.bases.error.api import ConflictError
from .schemas import GetSchema, PostSchema

endpoint = '/account'
tags = ['account']


@router.get(endpoint, tags=tags)
def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.session
    print(payload.search_text)
    return dict(success=True)


@router.post(endpoint, tags=tags)
async def create_account(payload: PostSchema, request: Request = None):
    session = request.state.async_session
    account_logic = AccountLogic(session)
    query = account_logic.get(payload.email)
    query = await session.execute(query)
    if query.fetchone():
        raise ConflictError('AccountExists')

    account = account_logic.create(
        email=payload.email,
        name=payload.name
    )

    await session.commit()
    return account.to_json()
