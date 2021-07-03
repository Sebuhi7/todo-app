from django.urls import path
from . import views

# app_name='todos'
urlpatterns = [
    path('todo_list/', views.todo_list_view, name='index'),
    path('delete/<int:todo_id>', views.delete, name='delete'),
    path('update/<int:todo_id>', views.update, name='update'),
    path('add/', views.add, name='add'),
    path("register/", views.register, name='register'),
    path('', views.login, name='login'),
    path('logout/', views.logout, name='logout' ),
    path('sent/<int:id>', views.sent_view, name="sent_user"),
    path('sent_to_view/', views.sent_from_view, name="sent_to_view"),
    path('sent_from_view/', views.sent_to_view, name="sent_from_view"),
]