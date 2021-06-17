from django.urls import path

from . import views as v


urlpatterns = [
    path('test', v.test),
]
