from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pd_main.urls')),
    re_path(
        r'^robots.txt$',
        TemplateView.as_view(
            template_name='pd_main/robots.txt', content_type='text/plain'
        ),
        name='robots_file',
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
