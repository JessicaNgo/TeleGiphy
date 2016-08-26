"""tele_giphy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# Django
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('game.urls')),
    # url(r'^game/', include('game.urls')),
    url(r'^admin/', admin.site.urls),
]

handler500 = 'tele_giphy.views.custom_error_page'
handler404 = 'tele_giphy.views.custom_not_found_page'
