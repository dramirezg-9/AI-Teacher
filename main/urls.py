from django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('features/', views.features, name='features'),
    path('solve/', views.solve, name='solve'),
    path('grade/', views.grade, name='grade')
]
