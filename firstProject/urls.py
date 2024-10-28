from django.contrib import admin
from django.urls import path, include  # Assurez-vous que 'include' est importé
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Inclure l'URL de l'application accounts
    path('accounts/', include('django.contrib.auth.urls')),  # URLs d'authentification intégrées
    path('', include('gestionLangue.urls')),  # Include the translate app's URLs

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
