import os
import time
from dotenv import load_dotenv
import redis


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
	time.sleep(0.01)
	msg = queue.get_message() # извлекаем сообщение
	if msg: # проверяем сообщение на пустоту
		if not isinstance(msg["data"], int): # проверяем, какой тип информации хранится в переменной data (msg имеет тип словаря)
			print(msg["data"]) 
