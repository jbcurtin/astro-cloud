import logging
import typing

from requests.auth import AuthBase
from requests.models import PreparedRequest

PWN: typing.TypeVar = typing.TypeVar('PWN')

logger = logging.getLogger(__file__)

class GCPAuth(AuthBase):
    def __call__(self: PWN, request: PreparedRequest) -> PreparedRequest:
        return request
