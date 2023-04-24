import json
import typing
from base64 import b64decode, b64encode

import itsdangerous
from itsdangerous.exc import BadSignature

from starlette.datastructures import MutableHeaders, Secret
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class SessionLoginMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        path: str = "/",
        https_only: bool = False,
    ) -> None:
        self.app = app
        self.path = path

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        connection = HTTPConnection(scope)
        user_session = connection.session

        await self.app(scope, receive, send)
