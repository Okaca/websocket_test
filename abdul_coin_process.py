#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate

import asyncio
import pathlib
import ssl
import requests
import websockets
import json
import time
from threading import Thread
def get_data_from_api(start,limit):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?&limit="+str(limit)+"&start="+str(start)

    payload={}
    headers = {
    'X-CMC_PRO_API_KEY': 'd7bba7a6-3164-4c9d-887a-037831f46402',
    'Accept': 'application/json'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code!=200:
        print("Respones is not 200")
        return -1
    else:
        return response.json()
raw_id_keys = []
start = 1
limit = 5000
coin_data = {}
response= get_data_from_api(start,limit)
if response!=-1:
    for item in response['data']:
        coin_data[str(item["id"])]={"name":item['name'],"symbol":item['symbol'],"slug":item["slug"]}
        raw_id_keys.append(item["id"])

async def receive_message(message):
    print(message)
async def consumer_handler(websocket):
    async for message in websocket:
        await receive_message(message)

async def send_list_task(coin_list):
    uri = "wss://stream.coinmarketcap.com/price/latest"
    async with websockets.connect(
        uri, ping_interval=None
    ) as websocket:
        string1 = {"method":"subscribe","id":"price","data":{"cryptoIds":coin_list,"index":None}}
        await websocket.send(json.dumps(string1))
        await consumer_handler(websocket)

loop = asyncio.new_event_loop()
for i in range(0, len(raw_id_keys), 100):
    loop.create_task(send_list_task(raw_id_keys[i:i+100]))
loop.run_forever()
