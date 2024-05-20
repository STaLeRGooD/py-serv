import os
import time
from dotenv import load_dotenv
import redis
import requests

load_dotenv()
REDIS_PASSWORD1 = os.getenv('REDIS_PASSWORD')

redis_client = redis.Redis(
    host='localhost',
    password=REDIS_PASSWORD1,
    port=6379, 
    db=0,
    decode_responses=True)

queue = redis_client.pubsub() 
queue.subscribe("task_end", "channelSecond")

while True:
	time.sleep(1)
	response = requests.get("http://localhost:8000/users")
	print(response.json())
