from django.urls import path
from .views import * 
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/',StuffList.as_view(), name='stuffs'),
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page = 'login'), name='logout'),
    path('register/',RegisterSection.as_view(), name='register'),
    path('task/<int:pk>', StuffDetail.as_view(), name='stuff'),
    path('create/', StuffCreate.as_view(), name='stuff-create'),
    path('update/<int:pk>', StuffUpdate.as_view(), name='stuff-update'),
    path('delete/<int:pk>', StuffDelete.as_view(), name='stuff-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),



]