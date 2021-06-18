from db_process import addCoinData, CoinDB, getCoinData
import requests
import websocket, json
import time
import _thread as thread
import threading
from datetime import datetime
import numpy as np
global raw_id_keys


"""def getCoinData():
    
    url = "https://web-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=2781,3526,3537,2821,3527,2782,3528,3531,3530,3533,3532,2832,3529,2783,2814,3549,2784,2786,2787,2820,3534,2815,3535,2788,2789,3536,3538,2790,3539,3540,3541,3542,2792,2793,2818,2796,2794,3544,3543,2795,3545,2797,3546,3551,3547,3550,3548,3552,3556,2800,2816,2799,3555,3558,3554,3557,3559,3561,2811,2802,3560,2819,2801,3562,2804,3563,2822,2803,2805,2791,3564,2817,2806,3566,3565,2808,2812,2798,3567,3573,3553,2807,2785,2809,3569,3568,2810,3570,2824,2813,3571,3572,2823,1,1027,2010,1839,6636,52,1975,2,512,1831,7083,74,9023,9022&convert_id=2781"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        
    if  response.status_code != 200:
        error = "Login Error => " + str(response.status_code)
        return -1

    return response.json()


data = getCoinData()
#print(data["data"].keys())"""


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


start = 1
limit = 5000
coin_data = {}
raw_id_keys = [-1]

response=get_data_from_api(start,limit)
if response!=-1:
    for item in response['data']:
        coin_data[str(item["id"])]={"name":item['name'],"symbol":item['symbol'],"slug":item["slug"]}
        raw_id_keys.append(item["id"])
    
else:
    print("HATA")
        
#print(raw_id_keys)
#print(coin_data[str(raw_id_keys[1])]["symbol"])

socket1 = "wss://stream.coinmarketcap.com/price/latest"

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(close_status_code, close_msg)

def on_open(ws):
    #def run(*args):
    string1 = {"method":"subscribe","id":"price","data":{"cryptoIds":raw_id_keys[1:100],"index":None}}
    ws.send(json.dumps(string1))
    #ws.send('{"method":"subscribe","id":"price","data":{"cryptoIds":'+str(raw_id_keys)+',"index":null} }')

def gen_keys(keys):
    gen = keys
    while(True):
        val = gen.next()

def on_message(ws, message):
    
    res = json.loads(message)
    coin_id=res["d"]["cr"]["id"]
    #if data != -1:
    name = coin_data[str(coin_id)]["name"]
    symbol = coin_data[str(coin_id)]["symbol"]
    slug  = coin_data[str(coin_id)]["slug"]

    p = res["d"]["cr"]["p"]
    v = res["d"]["cr"]["v"]
    t = res["d"]["t"]

    ts = round(t/1000)
    date = datetime.utcfromtimestamp(ts)

    print(coin_id,name, symbol,slug,p,v,date,ts)
    addCoinData(coin_id,name,symbol,slug,p,v,date,ts)

    

#websocket.enableTrace(True)

def connect_websocket():             
    ws = websocket.WebSocketApp(socket1,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close
                                )
    wst = threading.Thread(target=ws.run_forever)
    wst.daemon = True
    wst.start()

if __name__ == "__main__":
    try:
        connect_websocket()
    except Exception as err:
        print(err)
        print("connect failed")