from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.add_marksheet, name="add_marksheet"),
    path('view_sheets',views.view_sheets, name='view_sheets'),
    path('view_pychart/<str:id>',views.view_pychart, name='view_pychart'),



]