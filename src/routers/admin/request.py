from sqladmin import BaseView, expose, ModelView

from src.database.models import CategoryRequest
from src.helpers.permission import check_role_access, check_role_view


class RequestAdmin(ModelView, model=CategoryRequest):
    name = "Request"
    icon = "fa-chart-line"

    column_list = [CategoryRequest.id, CategoryRequest.description, CategoryRequest.status]
    column_labels = {CategoryRequest.id: "ID" ,CategoryRequest.description: "Description", CategoryRequest.status: "Status"}

    # form_columns = [CategoryRequest.name, CategoryRequest.description]
    column_details_exclude_list = [CategoryRequest.status]
    # @expose("/request-category", methods=["GET"])
    # def report_page(self, request):
    #     return self.templates.TemplateResponse(
    #         "request_admin.html",
    #         context={"request": request},
    #     )

    # def on_model_change(self, form, model, is_created):
    #     if is_created and isinstance(model, CategoryRequest):
    #         if model.status:
    #             category = CategoryModel(name=model.name, description=model.description, category_request_id=model.id)
    #             db.session.add(category)
    #             db.session.commit()
    #         else:
    #             raise HTTPException(status_code=400, detail="Request not approved")

    async def after_model_change(self, data, model: CategoryRequest, is_created: bool):
        pass
    def date_format(value):
        return value.strftime("%d.%m.%Y")



    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)
