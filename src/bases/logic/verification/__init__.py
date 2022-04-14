from copy import deepcopy
from uuid import uuid4

from src.bases.logic import Logic
from src.bases.error.core import CoreError
from src.models import (Verification)


class VerificationLogic(Logic):
    def get(self):
        pass