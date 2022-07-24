from kafka import KafkaProducer
import tweepy
import json


def connect_api():
    consumer_key = "consumer_key"
    consumer_secret = "consumer_secret"
    acces_token = "acces_token"
    acces_token_secret = "acces_token_secret"

    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, acces_token, acces_token_secret
    )

    api = tweepy.API(auth)
    return api

api = connect_api()

# query_list = ["오제제", "파델라", "회현식당"]
query = "맛짱조개"

# 브로커 생성 시에는 브로커의 호스트들의 리스트를 준비한다.
# 1개만 알아도 상관 없지만 모든 브로커들의 리스트를 입력하는 것을 권장
BROKER_SERVER = ["localhost:9092"]
# 토픽 네임
TOPIC_NAME = "twitter_topic"

producer = KafkaProducer(bootstrap_servers=BROKER_SERVER)


# 프로듀서 생성
tweets = api.search_tweets(q=query, count=500, result_type="recent", locale="kor")

tweet_list = []
for tweet in tweets:
    tweet_list.append(tweet.text)
for t in tweet_list:
    print(t)
    producer.send(TOPIC_NAME, json.dumps(t).encode("utf-8"))


producer.flush()

