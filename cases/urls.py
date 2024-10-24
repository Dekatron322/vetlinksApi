from django.urls import path
from . import views

urlpatterns = [
    path('cases/all/', views.list_all_cases, name='list-all-cases'),
    path('create-case/', views.create_case, name='create-case'),
    path('my-cases/', views.list_user_cases, name='my-cases'),
    path('cases/<int:case_id>/laboratory-report/', views.create_laboratory_report, name='create_laboratory_report'),
    path('cases/<int:case_id>/delete/', views.delete_case, name='delete-case'),  # Delete case endpoint
    path('cases/<int:case_id>/', views.get_case_detail, name='get-case-detail'),  # View case by ID
    path('cases/<int:case_id>/comments/', views.list_comments, name='list_comments'),
    path('cases/<int:case_id>/comments/add/', views.add_comment, name='add_comment'),
    path('cases/<int:case_id>/comments/<int:parent_comment_id>/reply/', views.add_comment, name='reply_to_comment'),
    path('comments/<int:comment_id>/replies/', views.list_replies, name='list_replies'),

]
