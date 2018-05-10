from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'locallibrary.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^account/', include('django.contrib.auth.urls')),
    
    
    url(r'^admin/', include(admin.site.urls)),
    url('^catalog/', include('catalog.urls')),
    url('', RedirectView.as_view(url='/catalog/', permanent=True)),
    
    
    
    
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)