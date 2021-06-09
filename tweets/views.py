from tweepy import API, OAuthHandler
from textblob import TextBlob
from tweepy.parsers import JSONParser
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from account.serializers import AccountSerializer
from rest_framework import status
from rest_framework.response import Response
from tweepy.parsers import JSONParser
import tweepy
import json
from django.shortcuts import render, HttpResponse
import requests
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from django.http import Http404


class TwitterClient(object):

    def __init__(self):

        consumer_key = 'IToiFc5IxJa6Yg3raLFaXFSwg'
        consumer_secret = 'KqsUA65fTX48EArpnnwqvrH9n57IIbToYssfdUs9RFxRdjyUr6'
        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            self.api = tweepy.API(self.auth)

        except requests.ConnectionError as err:
            err = 'Error: Authentication Failed'
            return Response({'error_connection': err})

    def clean_tweet(self, tweet):

        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ /  \ /  \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):

        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count):

        tweets = []

        try:

            fetched_tweets = tweepy.Cursor(self.api.search, q=query, rpp=100, count=20, result_type="recent",
                                           include_entities=True, lang="en").items(count)

            for tweet in fetched_tweets:

                parsed_tweet = {}

                parsed_tweet['text'] = tweet.text.encode('utf-8')
                parsed_tweet['created_at'] = tweet.created_at
                parsed_tweet['entities'] = tweet.entities
                parsed_tweet['username'] = tweet.user.screen_name.encode('utf-8')
                parsed_tweet['retweeted'] = tweet.retweeted
                parsed_tweet['profile_image'] = tweet.user.profile_image_url_https
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:

                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as err:
            raise Http404(err)


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def get_tweets(request):
    tweet_count = 250
    retrieve_count = 0
    try:
        if request.method == 'POST':
            search_id = request.POST['topic']
            if not search_id:
                return Response({"Please write any word for return tweets"})
            api = TwitterClient()

            tweets = api.get_tweets(query=search_id, count=tweet_count)

            ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

            ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

            result_positive = round((100 * len(ptweets) / len(tweets)), 1)

            result_negative = round((100 * len(ntweets) / len(tweets)), 1)

            result_neutral = round((100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)), 1)

            topic = "Sentiment analysis about \"" + search_id + "\""

            for i in tweets:
                retrieve_count = retrieve_count + 1
            data = {'tweet_count': tweet_count, 'result_positive': result_positive,
                    'result_negative': result_negative, 'result_neutral': result_neutral,
                    'topic': topic, 'retrieve_count': retrieve_count, 'tweets': tweets}

            return Response(data)
    except:
        return Response({"Not Fonud :("})
