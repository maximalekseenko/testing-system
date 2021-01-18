from django.conf.urls import url, include
from main.views import HomeView, HeresyoneView

urlpatterns = [
    url('heresyone/', HeresyoneView),
    url('', HomeView),
]