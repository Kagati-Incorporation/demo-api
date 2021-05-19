from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from core.views import home_view
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import  permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Demo API Documentation",
        default_version='v1',
        description="Documentation of Demo API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="info@kagati.io"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)
apipatterns = (
    [
        path('users/', include('users.urls')),
        path('common/', include('common.urls')),
        path('blogs/', include('blog.urls')),
        path('core/', include('core.urls')),
        path('newsletter/', include('newsletter.urls')),
        path('payments/', include('payments.urls')),
    ], 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title="Demo API", description="Demo API DOCS")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('api/', include(apipatterns)),
    path('', home_view),
    path('summernote/', include('django_summernote.urls')),


]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)