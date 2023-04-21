from sqladmin import ModelView
from src.database.models import RoleModel
from src.helpers.permission import check_role_access, check_role_view


class RoleAdmin(ModelView, model=RoleModel):
    column_list = [RoleModel.id, RoleModel.name]

    can_create = False
    can_delete = False
    can_edit = False
    can_export = False

    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)
