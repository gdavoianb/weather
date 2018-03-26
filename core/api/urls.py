from django.conf.urls import url, include

from core.api.router import router
from core.api.views import UploadAPI, DownloadAPI

urlpatterns = [
    url(r'^model/', include(router.urls)),
    url('^upload/?$', UploadAPI.as_view(), name='upload'),
    url('^download/?$', DownloadAPI.as_view(), name='download'),
]
