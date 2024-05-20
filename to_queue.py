import os
from dotenv import load_dotenv
load_dotenv()
import redis

REDIS_PASSWORD1 = os.getenv('REDIS_PASSWORD')

# аналогичное подключение к удаленному серверу Redis
connection = redis.Redis(
	host="localhost",
	password=REDIS_PASSWORD1,
	port=6379,
	db=0,
	decode_responses=True
)

connection.publish('channelFirst', 'Данное сообщение было отправлено в первый канал') # отправляем сообщение в первый канал
connection.publish('channelSecond', 'Данное сообщение было отправлено во второй канал') # отправляем сообщение во второй канал