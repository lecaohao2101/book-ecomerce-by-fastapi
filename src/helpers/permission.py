from starlette.requests import Request
from src.database.models import RoleModel, RoleEnum, UserModel
from src.database.session import SessionLocal


PERMISSION = {
    "ADMIN": [
        {"user-model": ["list", "details", "view"]},
        {"store-model": ["list","details","edit","delete","create"]},
        {"category-request": ["list","details","edit","delete","create"]},
        {"/": ["index"]},
    ],
    "STORE_OWNER": [
        {"book-model": ["list","details","edit","delete","create"]},
        {"category-model": ["list","details","edit","delete","create"]},
        {"order-model": ["list","details","edit","delete","create"]},
        {"order-item-model": ["list","details","edit","delete","create"]},
        {"category-request": ["list","details","edit","delete","create"]},
        {"/": ["index"]},
    ],
    "CUSTOMER": [],
}

VIEWS = {
    "ADMIN": [
        "user-model",
        "store-model",
        "category-request"
    ],
    "STORE_OWNER": [
        "book-model",
        "category-model",
        "order-model",
        "order-item-model",
        "category-request"
    ],
    "CUSTOMER": [],
}


def get_permission(role: str, resource: str, action: str):
    permissions: list[dict] = PERMISSION.get(role)
    if permissions:
        if permissions[0] != "*":
            count = 0
            for permission in permissions:
                permission_resource = permission.get(resource)
                if permission_resource:
                    if action in permission_resource:
                        count += 1
                    else:
                        continue
                else:
                    continue
            if count == 0:
                return False
            else:
                return True
        else:
            return True
    else:
        return False


def get_view(role: str, identity: str):
    view: list[dict] = VIEWS.get(role)
    if view:
        if view[0] == "*":
            return True
        elif identity in view:
            return True
        else:
            return False
    else:
        return False


def check_role_access(request: Request):
    role_request = request.session.get("role")
    session = SessionLocal()
    valid_role = session.query(RoleModel).get(role_request)
    if valid_role:
        path = request.url.path.strip("/").split("/")
        if len(path) > 2:
            resource = path[1]
            action = path[2]
            role = valid_role.name.value
            return get_permission(role, resource, action)
        elif len(path) == 1:
            resource = "/"
            action = "index"
            role = valid_role.name.value
            return get_permission(role, resource, action)
        elif len(path) == 2:
            resource = path[0]
            action = path[1]
            role = valid_role.name.value
            return get_permission(role, resource, action)
    else:
        return False


def check_role_view(request: Request, identity):
    role_request = request.session.get("role")
    session = SessionLocal()
    valid_role = session.query(RoleModel).get(role_request)
    if valid_role:
        role = valid_role.name.value
        return get_view(role, identity)
    else:
        return False




