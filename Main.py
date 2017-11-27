from TwitterAuth.AuthProvider import PTweepy

if __name__ == '__main__':
    api = PTweepy()
    screen_names = ['scifigene','gradiz_lenin','asmaabouderka','Isamarella']
    ids = ['1000004156', '1000010568', '100000801']
    temp1 = api.get_user_info_by_ids(ids)
    temp2 = api.get_user_info_by_screen_name(screen_names)
    temp3 = api.get_followers_by_screen_name(screen_names)
    temp4 = api.get_followers_by_id(ids)
    temp5 = api.get_friends_by_id(ids)
    temp6 = api.get_friends_by_screen_name(screen_names)