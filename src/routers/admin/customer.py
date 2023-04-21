from sqladmin import ModelView
from src.database.models import UserModel as CustomerModel
from src.helpers.permission import check_role_access, check_role_view


class CustomerAdmin(ModelView, model=CustomerModel):
    column_list = [CustomerModel.id, CustomerModel.email, CustomerModel.full_name, CustomerModel.role]
    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)