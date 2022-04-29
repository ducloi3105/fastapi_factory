from src.bases.api import Request, Depends
from src.bases.api.router import router
from src.logic.postgres.account import AccountLogic
from src.bases.error.api import ConflictError, BadRequestParams
from .schemas import GetSchema, PostSchema

endpoint = '/account'
tags = ['account']


@router.get(endpoint, tags=tags)
async def account(payload: GetSchema = Depends(GetSchema), request: Request = None):
    session = request.state.async_session
    account_logic = AccountLogic(session)
    query = await session.execute(
        account_logic.get(payload.email)
    )
    account = query.fetchone()
    if not account:
        raise BadRequestParams('AccountNotFound')

    account = account[0]
    print(123123, account.to_json())
    return dict(test=1)


@router.post(endpoint, tags=tags)
async def create_account(payload: PostSchema, request: Request = None):
    session = request.state.async_session
    account_logic = AccountLogic(session)
    query = await session.execute(
        account_logic.get(payload.email)
    )
    account = query.fetchone()
    if account:
        raise ConflictError('AccountExists')
    account = account_logic.create(
        email=payload.email,
        name=payload.name
    )

    await session.commit()
    return account.to_json()
