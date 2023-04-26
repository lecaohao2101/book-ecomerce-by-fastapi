from fastapi import HTTPException
from sqladmin import ModelView
from wtforms import PasswordField, Form

from src.database.models import UserModel
from src.helpers.permission import check_role_access, check_role_view

class MyForm(Form):
    password = PasswordField('New Password')

class UserAdmin(ModelView, model=UserModel):
    form = MyForm
    name_plural = "User"
    icon = "fa-solid fa-user"
    column_list = [UserModel.id, UserModel.email, UserModel.full_name, UserModel.role]




    column_details_exclude_list = [UserModel.list_order, UserModel.list_store, UserModel.list_address, UserModel.role_id]

    column_details_exclude_list = [
        UserModel.id,
        UserModel.role_id
    ]

    column_default_sort = [(UserModel.role_id, 1)]
    form_columns = [
        UserModel.email,
        UserModel.full_name,
        UserModel.password,
        UserModel.role
    ]

    column_labels = {UserModel.email: "Email", UserModel.full_name:"Full Name", UserModel.role:"Role"}

    column_details_exclude_list = [UserModel.password, UserModel.list_order, UserModel.list_store, UserModel.list_address, UserModel.role_id]
    can_create = False
    can_delete = False
    can_edit = True
    can_export = False

    def is_accessible(self, request) -> bool:
        return check_role_access(request)

    def is_visible(self, request) -> bool:
        return check_role_view(request, self.identity)






