from sqladmin import ModelView
from src.database.models import StoreModel
from src.helpers.permission import check_role_access, check_role_view


class StoreAdmin(ModelView, model=StoreModel):
    name_plural = "Store"
    icon = "fa-solid fa-store"

    # can_create = False
    # can_delete = False
    # can_edit = False
    # can_export = False

    column_list = [StoreModel.id, StoreModel.name, StoreModel.user]
    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)