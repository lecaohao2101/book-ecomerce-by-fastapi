from sqladmin import ModelView
from src.database.models import UserModel
from src.helpers.permission import check_role_access, check_role_view


class UserAdmin(ModelView, model=UserModel):

    name_plural = "User"
    icon = "fa-solid fa-user"
    column_list = [UserModel.id, UserModel.email, UserModel.full_name, UserModel.role]

    # exclude_properties = ['password']
    # form_extra_field = {
    #     'new_password': PasswordField('New Password')
    #
    # }
    # def on_model_change(self, data: dict, model: Any, is_created: bool) -> None:
    # def on_model_change(self, form, model, is_created) -> None:
    #     if form.new_password.data:
    #         model.password = generate_password_has(form.new_password.data)
    # column_details_exclude_list = [
    #     UserModel.id,
    #     UserModel.role_id
    # ]

    # column_default_sort = [(UserModel.role_id, 1)]
    # form_columns = [
    #     UserModel.email,
    #     UserModel.full_name,
    #     UserModel.password,
    #     UserModel.role
    # ]

    column_labels = {UserModel.email: "Email", UserModel.full_name:"Full Name", UserModel.role:"Role"}

    column_details_exclude_list = [UserModel.password]
    # column_exclude_list = [UserModel.password]
    can_create = False
    can_delete = False
    can_edit = True
    can_export = False

    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)


