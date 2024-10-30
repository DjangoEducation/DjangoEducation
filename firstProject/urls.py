from django.contrib import admin
from django.urls import path, include  # Assurez-vous que 'include' est importé
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('gestionCours/', include('gestionCours.urls')),
    path('chatbot/', include('chatbot.urls')),  # This allows the chatbot to be accessed from any route
    path('todo/', include('todo.urls')),  # This allows the chatbot to be accessed from any route

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
