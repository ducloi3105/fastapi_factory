import time
from contextvars import ContextVar


correlation_id: ContextVar[float] = ContextVar(
  'correlation_id', default=time.time()
)
