from os import getenv
import re

from dotenv import load_dotenv
import tweepy as twp
import pandas as pd
from flask import url_for, session, abort


def authenticate(host='app', on_callback=False):
    load_dotenv()  # import API access credential from .env file and loads into system environment variables
    if on_callback:
        auth = twp.OAuthHandler(getenv("CONSUMER_KEY"), getenv("CONSUMER_SECRET"))
        auth.request_token = {'oauth_token': session.get('request_token'),
                              'oauth_token_secret': session.get('oauth_verifier')}
        session.pop('request_token')
        session.pop('oauth_verifier')
        try:
            auth.get_access_token(verifier=auth.request_token['oauth_token_secret'])
        except twp.TweepError as e:
            print(e)
            print('Error! Failed to get access token.')
        else:
            return auth
    if host == 'client':
        auth = twp.OAuthHandler(getenv("CONSUMER_KEY"), getenv("CONSUMER_SECRET"), callback=url_for('main.search', host=host, _external=True))
        try:
            auth_redirect_url = auth.get_authorization_url()
        except twp.TweepError as e:
            print(e)
            return abort(500)
        else:
            session['request_token'] = auth.request_token['oauth_token']
            return auth_redirect_url
    elif host == 'app':
        auth = twp.AppAuthHandler(getenv("CONSUMER_KEY"), getenv("CONSUMER_SECRET"))
    elif host == 'admin':
        auth = twp.OAuthHandler(getenv("CONSUMER_KEY"), getenv("CONSUMER_SECRET"))
        auth.set_access_token(getenv("ACCESS_TOKEN"), getenv("ACCESS_TOKEN_SECRET"))

    return auth


def extract_tweets_from_q(query, api, use_pages=False, num=200):
    tweets = []
    if use_pages:
        for page in (twp.Cursor(api.search, q=query, result_type="mixed", lang="en", tweet_mode="extended").pages(num)):
            tweets = [[re.sub(r'http\S+', '', tw.retweeted_status.full_text),
                           tw.retweeted_status.created_at,
                           tw.retweeted_status.favorite_count,
                           tw.retweeted_status.user.location,
                           tw.retweeted_status.metadata["iso_language_code"],
                           tw.retweeted_status.retweet_count] if hasattr(tw, "retweeted_status") else [re.sub(r'http\S+', '', tw.full_text),
                                                                                                       tw.created_at,
                                                                                                       tw.favorite_count,
                                                                                                       tw.user.location,
                                                                                                       tw.metadata["iso_language_code"],
                                                                                                       tw.retweet_count] for tw in page]
    else:
        page = twp.Cursor(api.search, q=query, result_type="mixed", lang="en", tweet_mode="extended").items(num)
        tweets = [[re.sub(r'http\S+', '', tw.retweeted_status.full_text),
                   tw.retweeted_status.created_at,
                   tw.retweeted_status.favorite_count,
                   tw.retweeted_status.user.location,
                   tw.retweeted_status.metadata["iso_language_code"],
                   tw.retweeted_status.retweet_count] if hasattr(tw, "retweeted_status") else [re.sub(r'http\S+', '', tw.full_text),
                                                                                               tw.created_at,
                                                                                               tw.favorite_count,
                                                                                               tw.user.location,
                                                                                               tw.metadata["iso_language_code"],
                                                                                               tw.retweet_count] for tw in page]
    if len(tweets) == 0:
        return None
    tweets_df = pd.DataFrame(tweets, columns=["text", "date", "likes", "user_location", "language", "retweets"])
    tweets_df.drop_duplicates(subset='text', inplace=True)  # in case of duplicated tweets
    return tweets_df


def get_current_timeline(api):
    for i, tweet in enumerate(api.home_timeline()):
        print(i, tweet.text)
