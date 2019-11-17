import json
import logging

from django.shortcuts import get_object_or_404, render
from rest_framework import response, status, views, viewsets
from rest_framework.decorators import action

from api.v1.bot.models import Update
from api.v1.bot.serializers import UpdateSerializer


class GreetView(views.APIView):
    """A simple View for greeting newly-subscribed users."""

    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
    http_method_names = ['post']

    logger = logging.getLogger(__name__)

    def post(self, request):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        #if not ser.is_valid():
        #    # handle the validation errors
        #    # also if a bot joins the channel, see the UserSerializer
        #    pass

        updid = ser.validated_data.get('update_id')
        if updid:
            is_updated = True
            ser.save()
        else:
            is_updated = False

        return response.Response(
            data={'is_updated': is_updated},
            status=status.HTTP_200_OK,
            headers={'Content-Type': 'application/json'},
        )
