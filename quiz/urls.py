from django.urls import path
from . import views

urlpatterns = [
    path('quiz_page', views.quiz_page, name='quiz_page'),
    path('search/<str:category>', views.search_view, name='search'),
    path('<int:quiz_id>', views.quiz_view, name='quiz_view'),
]