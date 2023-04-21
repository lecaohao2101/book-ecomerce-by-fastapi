from typing import Optional

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.database.models import UserModel
from src.database.session import SessionLocal



class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        session = SessionLocal()
        valid_user = session.query(UserModel).filter_by(
            email=username
        ).first()
        session.close()
        if valid_user:
            if valid_user.password == password:
                request.session.update(
                    {"user_id": valid_user.id, "role": valid_user.role_id}
                )

                return True
            else:
                return False
        else:
            return False


    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        user_id = request.session.get("user_id")

        if not user_id:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
