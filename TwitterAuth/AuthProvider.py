import pandas as pd
import time
import tweepy
import math

WAIT_LIMIT = 5


def handle_error(f, *args, **kwargs):
    def wrapper(self, *args, **kwargs):
        while True:
            try:
                temp = f(self, *args, **kwargs)
                break
            except tweepy.RateLimitError:
                self.renew_key()
                continue
            except tweepy.error.TweepError as e:
                print(e)
                raise
            except Exception as e:
                print(e)
                raise
        return temp
    return wrapper


class PTweepy:
    """ PhongPhung: phongifls@gmail wrapper on tweepy for simple usage """
    _key_df = pd.read_excel('./TwitterAuth/Keys.xlsx')
    _key_df['check'] = time.time()

    request_counter = len(_key_df)

    def __init__(self):
        self.Api = None
        self.renew_key()

    def renew_key(self):
        self.request_counter -= 1
        if self.request_counter < 0:
            time.sleep(WAIT_LIMIT)
            self.request_counter = len(self._key_df)

        consumer_key, consumer_secret, access_token, access_token_secret, *_ = \
            list(self._key_df.iloc[self._key_df['check'].idxmin(), :])
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.Api = tweepy.API(auth)

    @handle_error
    def lookup_users(self, *args, **kwargs):
        temp = self.Api.lookup_users(*args, **kwargs)
        temp = pd.DataFrame(list(map(lambda x: x._json, temp)))
        return temp

    def get_user_info_by_screen_name(self, data):
        chunks = [data[y: y+100] for y in range(0, len(data), 100)]
        results = pd.DataFrame()
        for i in chunks:
            temp = self.lookup_users(screen_names=i)
            results = pd.concat([results, temp])
        results.reset_index(inplace=True, drop=True)
        return results

    def get_user_info_by_ids(self, data):
        data = list(map(str, data))
        chunks = [data[y: y + 100] for y in range(0, len(data), 100)]
        results = pd.DataFrame()
        for i in chunks:
            temp = self.lookup_users(user_ids=i)
            results = pd.concat([results, temp])
        results.reset_index(inplace=True, drop=True)
        return results

    @handle_error
    def friends_ids(self, *args, limit=-1, **kwargs):
        track_cursor = -1
        result = []
        count = 0
        if limit != -1:
            limit = math.ceil(limit/5000)
        cursor = tweepy.Cursor(self.Api.friends_ids, *args, cursor=track_cursor, **kwargs).pages()
        while count != limit:
            try:
                temp = next(cursor, None)
                track_cursor = cursor.next_cursor
                count += 1

                if temp is not None:
                    result.extend(temp)
                else:
                    break
            except tweepy.RateLimitError:
                self.renew_key()
                cursor = tweepy.Cursor(self.Api.friends_ids, *args, cursor=track_cursor, **kwargs).pages()

        final = pd.DataFrame(result, columns=['friends_id'])
        final['friends_id'] = final['friends_id'].apply(str)
        return final

    def get_friends_by_screen_name(self, data, info=False, limit=-1):
        results = pd.DataFrame()
        for i in data:
            temp = self.friends_ids(limit=limit, screen_name=i)
            temp['original_screen_name'] = i
            results = pd.concat([results, temp])
        if not info:
            return results
        temp = self.get_user_info_by_ids(list(results['friends_id']))
        results = pd.merge(left=results, right=temp, left_on='friends_id', right_on='id_str', how='left')
        return results

    def get_friends_by_id(self, data, info=False, limit=-1):
        results = pd.DataFrame()
        for i in data:
            temp = self.friends_ids(limit=limit, user_id=i)
            temp['original_sns_id'] = i
            results = pd.concat([results, temp])
        if not info:
            return results
        temp = self.get_user_info_by_ids(list(results['friends_id']))
        results = pd.merge(left=results, right=temp, left_on='friends_id', right_on='id_str', how='left')
        return results

    @handle_error
    def followers_ids(self, *args, limit=-1, **kwargs):
        track_cursor = -1
        result = []
        count = 0
        if limit != -1:
            limit = math.ceil(limit / 5000)
        cursor = tweepy.Cursor(self.Api.followers_ids, *args, cursor=track_cursor, **kwargs).pages()
        while count != limit:
            try:
                temp = next(cursor, None)
                track_cursor = cursor.next_cursor
                count += 1

                if temp is not None:
                    result.extend(temp)
                else:
                    break
            except tweepy.RateLimitError:
                self.renew_key()
                cursor = tweepy.Cursor(self.Api.friends_ids, *args, cursor=track_cursor, **kwargs).pages()

        final = pd.DataFrame(result, columns=['followers_id'])
        return final

    def get_followers_by_screen_name(self, data, info=False, limit=-1):
        results = pd.DataFrame()
        for i in data:
            temp = self.followers_ids(screen_name=i)
            temp['original_screen_name'] = i
            results = pd.concat([results, temp])
        if not info:
            return results
        temp = self.get_user_info_by_ids(list(results['followers_id']))
        results = pd.merge(left=results, right=temp, left_on='followers_id', right_on='id_str', how='left')
        return results

    def get_followers_by_id(self, data, info=False, limit=-1):
        results = pd.DataFrame()
        for i in data:
            temp = self.followers_ids(user_id=i)
            temp['original_sns_id'] = i
            results = pd.concat([results, temp])
        if not info:
            return results
        temp = self.get_user_info_by_ids(list(results['followers_id']))
        results = pd.merge(left=results, right=temp, left_on='followers_id', right_on='id_str', how='left')
        return results

