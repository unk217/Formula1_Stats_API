from django.urls import path, include
from rest_framework import routers
from . import views

routers = routers.DefaultRouter()
#routers.register(r'', EventViewSet, basename='events')
#routers.register(r'', ErgastRacesView.as_view(), basename='RaceView')

#urlpatterns = routers.urls
urlpatterns = [
    path("", views.consume_api_externa, name="f1-races"),
    # path("f1/races-async/", ErgastRacesAsyncView.as_view(), name="f1-races-async"),
]
