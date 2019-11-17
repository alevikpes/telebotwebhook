import logging

from django.core.exceptions import MultipleObjectsReturned
from rest_framework import serializers

from api.v1.bot.bot import Bot
from api.v1.bot.models import Update


class UserSerializer(serializers.Serializer):

    # https://core.telegram.org/bots/api#user

    id = serializers.IntegerField()
    is_bot = serializers.BooleanField()
    first_name = serializers.CharField(max_length=24)
    username = serializers.CharField(
        max_length=24, allow_blank=True, required=False)

    logger = logging.getLogger(__name__)

    def validate_is_bot(self, value):
        if value:
            msg = 'This user is a bot'
            self.logger.warning(msg)
            raise serializers.ValidationError(msg)

        return value


class ChatSerializer(serializers.Serializer):

    # https://core.telegram.org/bots/api#chat

    id = serializers.IntegerField()
    type = serializers.ChoiceField(
        ('private', 'group', 'channel', 'supergroup')
    )


class MessageSerializer(serializers.Serializer):

    # https://core.telegram.org/bots/api#message

    id = serializers.IntegerField()
    from_user = UserSerializer(required=False)
    date = serializers.IntegerField()
    chat = ChatSerializer()
    text = serializers.CharField(max_length=4096, allow_blank=True)
    new_chat_members = UserSerializer(required=False, many=True)

class UpdateSerializer(serializers.ModelSerializer):

    message = MessageSerializer()

    class Meta:
        model = Update
        fields = (
            'update_id',
            'message',
        )

    def save(self):
        valdata = self.validated_data
        upd_id = valdata.get('update_id')
        if not upd_id:
            return

        chat_id = self._get_chat_id(valdata)
        _, _ = Update.objects.update_or_create(
            chat_id=chat_id,
            defaults={'update_id': upd_id},
        )
        # send message to the channel, if new users subscribed
        message = valdata.get('message')
        new_users = message.get('new_chat_members')
        if new_users:
            # get chat id
            chat_id = message.get('chat').get('id')
            # instantiate a Bot object
            bot = Bot(chat_id)
            # send message to the new user in a channel
            #bot.send_tg_msg('Welcome to the channel')

    def validate_update_id(self, value):
        chat_id = self._get_chat_id(self.initial_data)
        try:
            upd = Update.objects.get(chat_id=chat_id)
        except Update.DoesNotExist:
            return value

        if value > upd.update_id:
            return value
        else:
            return

    def _get_chat_id(self, data):
        msg = data.get('message')
        chat = msg.get('chat')
        return chat.get('id')
