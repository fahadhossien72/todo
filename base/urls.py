from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.TaskList.as_view(), name='main'),
    path('detail/<str:pk>/', views.TaskDetail.as_view(), name='detail'),
    path('create/', views.TaskCreate.as_view(), name='task-create'),
    path('update/<str:pk>/', views.TaskUpdate.as_view(), name='task-update'),
    path('delete/<str:pk>/', views.TaskDelete.as_view(), name='task-delete'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),
]