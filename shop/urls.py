from django.urls import path,include
from . import views

app_name='shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path("loguser/", views.login_user, name="loguser"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('developer/', views.developer_view, name='developer'),
    path('search/', views.search, name='search'),
    path('games/<int:game_id>/play/', views.play_game, name='play_game'),
    path('games/<int:game_id>/info', views.game_info, name='game_info'),
    path('developer/publish/', views.publish_page_view, name='publish'),
    path('developer/publish_game/', views.create_game, name='publish_game'),
    path('developer/mygames/', views.developer_games, name='developer_games'),
    path('developer/games/<int:game_id>/edit/', views.edit_game, name='editgame'),
    path('developer/games/<int:game_id>/update/', views.edit_game_update, name='updategame'),
    path('developer/games/<int:game_id>/delete/', views.edit_game_delete, name='deletegame'),
]
