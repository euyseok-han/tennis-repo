from django.urls import path
from . import views

app_name = 'match'
urlpatterns = [
    path('index', views.IndexView.as_view(), name='index'),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path('write/', views.write, name='write'),
    path('confirm/', views.confirm, name='confirm'),
    path('', views.loginUser, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logoutUser, name='logout')
]
