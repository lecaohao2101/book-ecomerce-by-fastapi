from sqladmin import BaseView, expose, ModelView

from src.database.models import CategoryRequest
from src.helpers.permission import check_role_access, check_role_view


class RequestAdmin(ModelView, model=CategoryRequest):
    name = "Request"
    icon = "fa-chart-line"

    # @expose("/request-category", methods=["GET"])
    # def report_page(self, request):
    #     return self.templates.TemplateResponse(
    #         "request_admin.html",
    #         context={"request": request},
    #     )

    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)
