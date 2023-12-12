from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('add_project/', add_project_page, name='add_project'),
    path('delete_project/<int:project_id>', delete_project),
    path('account/', account_page, name='account'),
    path('delete_avatar/', delete_avatar, name='delete_avatar'),
    path('project/<int:project_id>', project_detail_page),
    path('hide_modal', modal_hided, name='hide_modal'),
]