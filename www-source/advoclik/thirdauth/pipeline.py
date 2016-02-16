__author__ = 'p_kravik'

from .models import facebook_data
import requests
from django.http import HttpResponse




def get_friend_count(backend, user, response, *args, **kwargs):
    if backend.name == 'facebook':

        social_user = user.social_auth.filter(provider='facebook').first()
        url = u'https://graph.facebook.com/{0}/friends'.format(social_user.uid)

        r = requests.get(url, params={'access_token': social_user.extra_data['access_token']})
        json_response = r.json()

        num_friends = json_response['summary']['total_count']
        name = social_user.extra_data['name']

        updated_values = {'friend_count': num_friends,
                          'name': name}

        fb_data, created = facebook_data.objects.update_or_create(user_id=user.id,
                                                                  defaults=updated_values)


