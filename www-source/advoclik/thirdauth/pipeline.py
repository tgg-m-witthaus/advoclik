__author__ = 'p_kravik'

from .models import facebook_data

def get_friend_count(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':
        new_data = facebook_data(user=user.id,
                                 friend_count=0,
                                 name="bob")

        new_data.save()

