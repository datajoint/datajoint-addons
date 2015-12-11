from slacker import Slacker
import datajoint as dj
from functools import wraps


class notify_user:
    """
    Decorator that notifies a user in a direct message when the table is done populating.

    Needs a slack API-Token and internet access to work.
    """
    def __init__(self, user, api_token):
        slack = Slacker(api_token)

        users = slack.users.list()
        assert users.successful, "Could not get user list"

        users = [u for u in users.body['members'] if u['name'] == user]
        assert len(users) == 1, "Could not identify user"

        self.user = users[0]
        self.slack = slack

    def __call__(self, cls):
        assert issubclass(cls, (dj.Computed, dj.Imported)), "notify can only decorate Computed and Imported tables"
        cls.__make_tuples = cls._make_tuples # move _make_tuples out of the way

        @wraps(cls.__make_tuples)
        def _make_tuples(itself, key):
            itself.__make_tuples(key)
            left, _ = itself.progress()

            if left == 0:
                ch = self.slack.im.open(self.user['id'])
                if ch.successful:
                    self.slack.chat.post_message(channel=ch.body['channel']['id'],
                                            text='Hey %s! Just to let you know. I am done with populating %s.'
                                                 % (self.user['name'], cls.__name__),
                                            username='J.A.R.V.I.S.',
                                            icon_emoji=':thought_balloon:')
                self.slack.im.close(ch.body['channel']['id'])

        cls._make_tuples = _make_tuples

        return cls
