from django.urls import path
from . import views

app_name = 'showcase'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('category/<slug:slug>/', views.category_detail_view, name='category_detail'),
    path('project/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('inquiry/submit/', views.submit_inquiry_view, name='submit_inquiry'),
]
