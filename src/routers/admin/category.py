from sqladmin import ModelView
from src.database.models import CategoryModel
from src.helpers.permission import check_role_access, check_role_view


class CategoryAdmin(ModelView, model=CategoryModel):
    name_plural = "Category"
    icon = "fa-solid fa-category"
    column_list = [CategoryModel.id, CategoryModel.name]
    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)