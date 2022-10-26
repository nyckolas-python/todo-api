from django.urls import path
from api import views


urlpatterns = [
    path('login/', views.user_login),
    path('create-user/', views.RegisterUserView.as_view()),
    path('v1/task/', views.TaskListView.as_view()),
    path('v1/task/<int:pk>', views.TaskDetailView.as_view(),
         name='task_update'),
    path('v1/create-images/', views.CreateImagesView.as_view(),
         name='img_create'),
]