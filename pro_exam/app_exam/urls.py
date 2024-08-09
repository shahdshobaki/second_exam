from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('add_idea', views.add_idea),
    path('logout', views.logout),
    path('update/<int:id>/', views.update),
    path('update_idea/<int:idea_id>/', views.update_idea),
    path('delete', views.delete),
    path('idea/<int:id>/', views.idea_detail),
]
