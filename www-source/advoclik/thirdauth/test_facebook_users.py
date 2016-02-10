__author__ = 'p_kravik'

import requests
import time
import itertools

APP_ID = "518130741701742"
APP_SECRET = "5cb06206d0c08cb3f0809d533f4a7a5e"


def get_app_access_token():
    access_token_url = "https://graph.facebook.com/oauth/access_token"
    r = requests.get(access_token_url, params={'client_id': APP_ID, 'client_secret': APP_SECRET, 'grant_type': "client_credentials"})
    app_access_token = r.text.split("=")[1]
    return app_access_token


def make_two_users_friends(user1, user2):
    user1_token = user1['access_token']
    user1_id = user1['id']
    user2_token = user2['access_token']
    user2_id = user2['id']


    first_invite_url = "https://graph.facebook.com/v2.5/" +  user1_id + "/friends/" + user2_id
    r1 = requests.post(first_invite_url, params={'access_token': user1_token})

    second_invite_url = "https://graph.facebook.com/v2.5/" +  user2_id + "/friends/" + user1_id
    r2 = requests.post(second_invite_url, params={'access_token': user2_token})

    if r1.status_code != 200:
        print "r1: got status code %d" % (r.status_code)

    if r2.status_code != 200:
        print "r2: got status code %d" % (r.status_code)



def create_test_users(app_access_token, user_name_array):
    url = "https://graph.facebook.com/v2.5/" + APP_ID + "/accounts/test-users"

    user_options = {'installed': True,
                    'permissions': ['email', 'user_friends', 'public_profile']}

    user_options['access_token'] = app_access_token

    for name in user_name_array:
        user_options['name'] = name
        r = requests.post(url, params=user_options)
        time.sleep(1)


def get_test_users(app_access_token):
    url = "https://graph.facebook.com/v2.5/" + APP_ID + "/accounts/test-users"
    r = requests.get(url, params={'access_token': app_access_token})
    test_users = r.json()['data']
    return test_users


def delete_all_test_users(app_access_token):
    url = "https://graph.facebook.com/v2.5/" + APP_ID + "/accounts/test-users"
    r = requests.get(url, params={'access_token':app_access_token})
    test_users = r.json()['data']

    if len(test_users) > 0:
        print "deleting %d test users" % (len(test_users))
        for user in test_users:
            delete_test_user(user['id'], user['access_token'])
            time.sleep(1)


def delete_test_user(user_id, user_token):
    r = requests.delete("https://graph.facebook.com/v2.5/" + str(user_id), params={'access_token': user_token})
    if r.status_code != 200:
        print "got status code %d" % (r.status_code)

if __name__ == '__main__':

    app_access_token = get_app_access_token()

    delete_all_test_users(app_access_token)

    test_name_array = ['Paul Kravik', 'Miles Witthaus', 'Cody Cook', 'William Ryan']
    create_test_users(app_access_token, test_name_array)

    test_user_list = get_test_users(app_access_token)

    for user1, user2 in itertools.combinations(test_user_list, 2):
        make_two_users_friends(user1, user2)




