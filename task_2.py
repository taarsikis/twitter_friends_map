""" Github: """
import requests


def twitter_api(nickname,bearer_token):
    """
    Returns info from twitter API.
    """
    base_url = "https://api.twitter.com/"

    search_url = '{}1.1/friends/list.json'.format(base_url)

    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }

    search_params = {
        'screen_name': nickname,
        'count':10
    }

    response = requests.get(search_url, headers = search_headers, params=search_params)
    return response


if __name__ == "__main__":
    user_nickname = input("Write your twitter nickname:")
    token = input("write your Bearer token:")
    response = twitter_api(user_nickname,token)
    needed_users = response.json()
    while True:
        print("Chose one of next categories:")
        print(list(needed_users.keys()))
        needed_category = input("Wich one?  ")
        if isinstance(needed_users[needed_category], list):
            print("There is the list.")
            max_idx = len(needed_users[needed_category])
            if max_idx == 0:
                print("But there is nothing.")
                break
            else:
                index = int(input("Chose the index of list item ( from 0 to {} ):".format(max_idx)))
                needed_users = needed_users[needed_category][index]

        elif isinstance(needed_users[needed_category], dict):
            print("There is the dictionary. Please choose one of categories.")
            print(list(needed_users[needed_category].keys()))
            needed_category_new = input("Wich one?  ")

            needed_users = needed_users[needed_category][needed_category_new]
        else:
            print("It is... ",needed_users[needed_category])
            break
    print("Thanks for using my program!")
