from fastapi import FastAPI
import clickhouse_connect
import json
import os
from dotenv import load_dotenv
load_dotenv()
import redis
from fastapi.responses import RedirectResponse
import requests

DB_PASSWORD = os.getenv('DB_PASSWORD')

client = clickhouse_connect.get_client(host='localhost', username='default', password=DB_PASSWORD)

REDIS_PASSWORD1 = os.getenv('REDIS_PASSWORD')

redis_client = redis.Redis(
    host='localhost',
    password=REDIS_PASSWORD1,
    port=6379, 
    db=0,
    decode_responses=True)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/task")
def read_root():
    length = redis_client.llen("task_list")
    print(length)
    if length != 0:
        value = redis_client.lpop("task_list")
        #length = redis_client.hvals("task_list:")
        test2 = redis_client.hgetall('task_list:'+ value)
        redis_client.hdel('task_list:'+ value,"ipv4","mac")
        return {"user": test2}
    else:
        return {"user": []}
        

@app.get("/users")
#{ipv4};{mac}
#ipv4: str, mac: str
def read_users():
    response = requests.get("http://localhost:8000/task")
    data_json = response.json()
    if len(data_json["user"]) != 0:
        mac = data_json["user"]["mac"]
        ipv4 = data_json["user"]["ipv4"]
        parameters = {'mac': mac, 'ipv4': ipv4}
        result_ip = client.command("SELECT username FROM users.users WHERE mac == {mac:String} AND ipv4 == {ipv4:String}", parameters=parameters)
        if  len(result_ip) != 0:
            redis_client.publish('task_end', str(data_json)) # отправляем сообщение в первый канал
            return {"user": data_json}
        else:
            return {"user": "not found"}
    else:
        return {"queue is empty"}