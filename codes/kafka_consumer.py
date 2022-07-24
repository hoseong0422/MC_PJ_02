from kafka import KafkaConsumer
import json
import pymongo

client = pymongo.MongoClient("몽고디비 연결정보 입력")
client
db = client.tweet

BROKER_SERVER = ["localhost:9092"]
TOPIC_NAME = "twitter_topic"

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BROKER_SERVER)

tweet_list = []
# consumer는 파이썬의 Generator로 구성되어 있다.
print("Wait....")
for message in consumer:
    tweet = json.loads(message.value.decode())
    doc = {"tweet" : tweet}
    db.tweet.insert_one(doc)

print("Done....")

