from fastapi import Request
from starlette.middleware.sessions import SessionMiddleware

from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from src.config import settings
from src.database.models import CategoryRequest
from src.routers.admin.address import AdressAdmin
from src.routers.admin.authentication import AdminAuth
from src.routers.admin.author import AuthorAdmin
from src.routers.admin.book import BookAdmin
from src.routers.admin.category import CategoryAdmin
from src.routers.admin.order import OrderAdmin
from src.routers.admin.order_item import OrderItemAdmin
from src.routers.admin.user import UserAdmin
from src.routers.admin.store import StoreAdmin
from src.routers.admin.request import RequestAdmin

from src.routers.ui_routes import router as ui_router, TEMPLATES
from src.routers.products import router as product_router
from src.database.models.address import AddressModel
from src.database.session import *

from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from src.database.models import UserModel


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="app-dev")
templates = Jinja2Templates(directory="templates")

# if settings.debug == 'True':
#     app = FastAPI(debug=True, reload=True)
# else:
#     app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(ui_router)
app.include_router(product_router)

# ADMIN
authentication_backend = AdminAuth(secret_key="app-dev")
admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
    templates_dir="src/templates"
)


admin.add_view(UserAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(AuthorAdmin)
admin.add_view(AdressAdmin)
admin.add_view(OrderAdmin)
admin.add_view(StoreAdmin)
admin.add_view(BookAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(RequestAdmin)


@app.post("/register")
async def register(
        request: Request,
        role_id: int = Form(default=3),
        email: str = Form(default=None),
        full_name: str = Form(default=None),
        password: str = Form(default=None),
        re_password: str = Form(default=None),
        session: Session = Depends(get_db)
):
    if password != re_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password does not match")

    user = UserModel(role_id=role_id, email=email, full_name=full_name, password=password)
    session.add(user)
    session.commit()
    user_id_pk = user.id
    return TEMPLATES.TemplateResponse("pages/page-address.html", {
        "request": request,
        "config": settings,
        "user_id": user_id_pk
    })


@app.post("/register_address")
async def register(
        request: Request,
        user_id: int = Form(default=None),
        country: str = Form(default="Việt Nam"),
        city: str = Form(default="Hà Nội"),
        district: str = Form(default="Ba Đình"),
        ward: str = Form(default="Điện Biên"),
        street: str = Form(default="Chu Văn An"),
        number_home: int = Form(default=123),
        session: Session = Depends(get_db)
):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID is required")

    address = AddressModel(
        country=country,
        city=city,
        district=district,
        ward=ward,
        street=street,
        number_home=number_home
    )

    address.user_id = user_id
    session.add(address)
    session.commit()
    return RedirectResponse(url="/page-sign-in", status_code=status.HTTP_302_FOUND)



@app.post('/login')
async def login(
        request: Request,
        email: str = Form(default=None),
        password: str = Form(default=None),
        db: Session = Depends(get_db)
):
    valid_user = db.query(UserModel).filter(
        UserModel.email == email
    ).first()

    if valid_user:
        if valid_user.password == password:
            request.session.update(
                {"user_id": valid_user.id, "role": valid_user.role_id}
            )
            return RedirectResponse(url="/stores/", status_code=status.HTTP_302_FOUND)
    return TEMPLATES.TemplateResponse("pages/page-sign-in.html", {
        "request": request,
        "message": "Invalid information login"
    })


