"""hakathon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import include
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from hakathon.router import router


app_name = 'hakathon'
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api/', include((router.urls, 'router'), namespace='api')),
]

if settings.ENABLE_DOCS:
    schema_view = get_schema_view(
        openapi.Info(
            title="Hakathon Swagger API",
            default_version='v1',
            description="API for autogenerator",
       ),
       public=True,
       permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        re_path('^docs-swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('docs-swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('docs-redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
        path('docs/', include_docs_urls(title='Hakathon API', permission_classes=[])),
    ]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
