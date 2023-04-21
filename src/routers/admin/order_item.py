from sqladmin import ModelView
from src.database.models import OrderItemModel
from src.helpers.permission import check_role_access, check_role_view


class OrderItemAdmin(ModelView, model=OrderItemModel):
    name_plural = "Order Item"
    icon = "fa-solid fa-order-item"
    column_list = [OrderItemModel.id, OrderItemModel.book, OrderItemModel.order, OrderItemModel.quantity, OrderItemModel.subtotal]
    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)