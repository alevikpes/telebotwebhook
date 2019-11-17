from django.urls import include, path


urlpatterns = [
    path('bot/', include('api.v1.bot.urls')),
]
