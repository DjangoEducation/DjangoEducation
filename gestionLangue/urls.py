from django.urls import path
from . import views

urlpatterns = [
    path('translate/', views.gradio_view, name='gradio_view'),
]
