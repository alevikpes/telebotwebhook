from django.db import models


class Update(models.Model):

    # https://core.telegram.org/bots/api#update

    update_id = models.IntegerField(unique=False)
    chat_id = models.IntegerField()
