from django.urls import path

from api.v1.bot import views
from teleautobot import settings


urlpatterns = [
    path(
        r'%s/' % settings.BOT_TOKEN,
        views.GreetView.as_view(),
        name='bot',
    )
]
