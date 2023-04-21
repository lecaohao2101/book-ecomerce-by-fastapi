from sqladmin import ModelView
from src.database.models import OrderModel
from src.helpers.permission import check_role_access, check_role_view


class OrderAdmin(ModelView, model=OrderModel):
    name_plural = "Order"
    icon = "fa-solid fa-order"
    column_list = [OrderModel.id, OrderModel.created_date, OrderModel.total]

    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)