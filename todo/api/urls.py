from django.urls import path
from .views import taskview
from .views import taskdetail,taskcreate,taskupdate,taskdelete,customloginview,LogoutView,registerpage


urlpatterns=[
    path('login/',customloginview.as_view(),name='login'),
    path('register/',registerpage.as_view(),name='register'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('',taskview.as_view(),name='tasks'),
    path('task/<int:pk>/',taskdetail.as_view(),name='taskdetail'),
    path('create-task/',taskcreate.as_view(),name='task-create'),
    path('update-task/<int:pk>/',taskupdate.as_view(),name='task-update'),
    path('delete-task/<int:pk>/',taskdelete.as_view(),name='task-delete'),

]