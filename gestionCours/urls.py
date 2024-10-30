from django.urls import path
from . import views

urlpatterns = [
    path('course/', views.courses_list, name='courses_list'),
    path('courses-add', views.add_course, name='courses_add'),
    path('courses/<int:course_id>/update/', views.update_course, name='courses_update'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='courses_delete'),
    path('course/<int:course_id>', views.courses_selectionner, name='courses_selectionner'),
    path('course/<int:course_id>/chapitre/add/', views.add_chapitre, name='add_chapitre'),
    
]
