from django.shortcuts import render

# Create your views here.
from tweepy import API, OAuthHandler

from textblob import TextBlob

from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from account.serializers import AccountSerializer


# from API_KEYS import api_key, api_secret_key

def clean_tweets(tweet):
    tweet_words = str(tweet).split(' ')
    clean_words = [word for word in tweet_words if not word.startswith('#')]
    return ' '.join(clean_words)


def analyze(Topic):
    api_key = 'IToiFc5IxJa6Yg3raLFaXFSwg'

    api_secret_key = 'KqsUA65fTX48EArpnnwqvrH9n57IIbToYssfdUs9RFxRdjyUr6'

    positive_tweets, negative_tweets, all_tweets = [], [], []
    authentication = OAuthHandler(api_key, api_secret_key)
    api = API(authentication)
    public_tweets = api.search(Topic, count=1000)
    # add it
    all_tweets = [clean_tweets(tweet) for tweet in public_tweets]  # clean_tweets(tweet.text)

    cleaned_tweets = [clean_tweets(tweet.text) for tweet in public_tweets]  # clean_tweets(tweet.text)
    for tweet in cleaned_tweets:
        tweet_polarity = TextBlob(tweet).sentiment.polarity
        if tweet_polarity < 0:
            negative_tweets.append(tweet)
            continue
        positive_tweets.append(tweet)

    for tweet in negative_tweets:
        print(tweet)
    for tweet in positive_tweets:
        print(tweet)
    for tweet in all_tweets:
        print(tweet)

    return positive_tweets, negative_tweets, all_tweets


# positive, negative = analyze('mohamed')
# # print(positive , '\n\n', negative)
# print(len(positive), ' VS  ', len(negative))


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def get_tweets(request):
    topic = request.POST['topic']
    positive, negative, all_tweets = analyze(topic)
    data = {}

    data['negative_count'] = len(negative)
    data['positive_count'] = len(positive)
    data["positive"] = positive
    data["negative"] = negative
    data['all_tweets'] = all_tweets

    return Response(data)

# @api_view(['GET', ])
# @permission_classes([IsAuthenticated])
# def search(request):
#     api_key = 'IToiFc5IxJa6Yg3raLFaXFSwg'
#
#     api_secret_key = 'KqsUA65fTX48EArpnnwqvrH9n57IIbToYssfdUs9RFxRdjyUr6'
#
#     authentication = OAuthHandler(api_key, api_secret_key)
#
#     api = API(authentication)
#
#     corona_tweets = api.search('corona virus')
#
#     for tweet in corona_tweets:
#         text = tweet.text
#         print(text)
#         # return HttpResponse(text)
#     return Response("ok")

# search()
