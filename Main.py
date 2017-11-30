from TwitterAuth.AuthProvider import PTweepy

if __name__ == '__main__':
    api = PTweepy()
    screen_names = ['asmaabouderka','Isamarella']
    ids = ['1000004156', '1000010568']
    temp1 = api.get_user_info_by_ids(ids)
    temp2 = api.get_user_info_by_screen_name(screen_names)
    temp3 = api.get_followers_by_screen_name(screen_names, info=True, limit=10000)
    temp4 = api.get_followers_by_id(ids, info=True, limit=5000)
    temp5 = api.get_friends_by_id(ids, info=True, limit=10000)
    temp6 = api.get_friends_by_screen_name(screen_names, info=True, limit=10000)
    print('{}, {}, {}, {}, {}, {}'.format(temp1, temp2, temp3, temp4, temp5, temp6))