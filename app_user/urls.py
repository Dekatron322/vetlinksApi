from django.urls import path
from app_user.views import *

app_name = "app_user"

urlpatterns = [
    path('sign-up/', sign_up, name='sign_up'),
    path('sign-in/', sign_in, name='sign_in'),
    path('all/', all, name='all'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),

    path('get-user-detail/<int:user_id>/', get_user_detail, name='get_user_detail'),

]
