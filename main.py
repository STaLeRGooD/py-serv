from fastapi import FastAPI
import clickhouse_connect
import json
import os
from dotenv import load_dotenv

load_dotend()

DB_PASSWORD = os.getenv(DB_PASSWORD)
client = clickhouse_connect.get_client(host='localhost', username='default', password=DB_PASSWORD)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/users/{ipv4};{mac}")
def read_users(ipv4: str, mac: str):
    parameters = {'mac': mac, 'ipv4': ipv4}
    result_ip = client.command("SELECT username FROM users.users WHERE mac == {mac:String} AND ipv4 == {ipv4:String}", parameters=parameters)
    return {"username": result_ip}
