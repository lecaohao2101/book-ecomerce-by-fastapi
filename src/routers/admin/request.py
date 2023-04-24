from sqladmin import BaseView, expose, ModelView

from src.database.models import CategoryRequest
from src.helpers.permission import check_role_access, check_role_view


class RequestAdmin(ModelView, model=CategoryRequest):
    name = "Request"
    icon = "fa-chart-line"

    column_list = [CategoryRequest.id, CategoryRequest.description, CategoryRequest.status]
    column_labels = {CategoryRequest.id: "ID" ,CategoryRequest.description: "Description", CategoryRequest.status: "Status"}

    # column_details_exclude_list = [CategoryRequest.status]
    # @expose("/request-category", methods=["GET"])
    # def report_page(self, request):
    #     return self.templates.TemplateResponse(
    #         "request_admin.html",
    #         context={"request": request},
    #     )

    def date_format(value):
        return value.strftime("%d.%m.%Y")



    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)
