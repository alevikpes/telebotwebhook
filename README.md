# teleautobot

Telegram bot for a webhook implementation.

See [this guide](https://core.telegram.org/bots/webhooks) for webhook setup.



### Implementation

This application is implemented in **Django** version 2.2.7 and **Django Rest
Framework** version 3.10.3. See also `requirements.txt` for more info.

It uses SQLite database for storing the `update_id` and the corresponding
`chat_id` for every chat, which is required for catching the updates.
Nothing else is stored (we value the privacy of the users).

**WARNING** There are no unit tests yet.


### Environment setup

This environment uses **Docker** and **docker-compose**. See the
corresponding web pages for details. See also
[this](https://github.com/alevikpes/utils/tree/master/docker) for setup
instructions.


### Secrets

All secrets are stored in a file `./environments/.env`, which is added to
the `.gitignore`. Create this file in your environment with the correct data:
```
# django
ALLOWED_HOSTS=localhost
DJANGO_SETTINGS_MODULE=teleautobot.settings
DEBUG=True
ENVIRONMENT=local
SECRET_KEY=<your secret key>

# bot data
BOT_NAME=<your bot name>
BOT_TOKEN=<your bot token>
```


### Test the app

Fire up the docker containers and make a curl request similar to this:
```bash
curl -X POST \
    http://localhost:8008/api/v1/bot/<your bot token>/ \
    -H 'Content-Type: application/json' \
    -d '{ \
        "update_id": "1", \
        "message": { \
            "id": "1", \
            "date": "334563635645", \
            "text": "This is the text of the message", \
            "chat": { \
                "id": "1", \
                "type": "group"}, \
            "new_chat_members": [ \
                { \
                    "id": "2", \
                    "is_bot": false, \
                    "first_name": "First Name 2" \
                } \
            ] \
        } \
    }'
```
You must recieve one of the `Updated`, `No updates` messages as a response.

For details see the serializer file.


### Tips

To get a chat id, add the bot to the chat and write at list one message to
that chat. Then make request to get updates:
```bash
curl -X POST https://api.telegram.org/bot<your bot token>/getUpdates
```
The response will contain the chat id among the other data:
```json
{
    "ok": true,
    "result": [
        {
            "update_id": 804602257,
            "channel_post": {
                "message_id": 2,
                "chat": {
                    "id": -1081334363939,  <-- chat id is here
                    "title": <chat name>,
                    "type": "channel"
                },
                "date": 1577047340,
                "text": "hi"
            }
        }
    ]
}
```
