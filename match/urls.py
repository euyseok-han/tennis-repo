from django.urls import path

from . import views

app_name = 'match'
urlpatterns = [
    path('index', views.index, name='index'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('write/', views.write, name='write'),
    path('', views.loginUser, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('conversation/<int:post>/<int:host>/<int:guest>/',
         views.conversation,
         name='conversation'),
    path('conversation/', views.conversation_list, name='conversation_list'),
    path('profile/<int:pk>', views.user_profile, name='profile'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_post/<int:pk>', views.update, name='update'),
    path('delete/<int:pk>', views.delete, name='delete'),
]
