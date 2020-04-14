from django.urls import path,include
from . import views

app_name='shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('loguser/', views.login_user, name='loguser'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name="home"),
    path('catalog/', views.catalog_view, name="catalog"),
]
