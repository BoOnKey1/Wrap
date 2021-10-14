# -*- coding: utf-8 -*-
 
import websocket
import _thread
import time
import json
import pandas as pd

def on_message(ws, message):
    message = json.loads(message)
    type_ = message["type"]
    if type_ == "snapshot":
        global asks_
        global bids_
        asks_ = pd.DataFrame({i: {"prix": message["asks"][i][0], "quantity": message["asks"][i][1]} 
            for i in range(len(message["asks"]))}).T.astype(float).set_index("prix")
        bids_ = pd.DataFrame({i: {"prix": message["bids"][i][0], "quantity": message["bids"][i][1]} 
            for i in range(len(message["bids"]))}).T.astype(float).set_index("prix")
        set_best_prices()

    if type_ == "l2update":
         change = message["changes"][0]
         do_update_order_book(asks_, bids_, change)
         set_best_prices()
         
         
def do_update_order_book(asks_, bids_, change):
     if "buy" in change:
         do_update_data(bids_, change)         
     if "sell" in change:
         do_update_data(asks_, change)
 
def do_update_data(frame, change):
   prix = float(change[1])
   qty = float(change[2])
   if prix in list(frame.index):
       if qty == 0:
           frame.drop(labels=prix,axis=0,inplace=True)
           return frame.sort_index()
       else: 
           frame.loc[prix]=qty
           return frame.sort_index
       
def set_best_prices():
    best = {"best ask":min(list(asks_.index)),"best bid":max(list(bids_.index)), "spread":(min(list(asks_.index)) - max(list(bids_.index)))}
    print(best)
   
def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
#    print(asks_)
#    print(bids_)
    print("### closed ###")
          
def create_subscribe():
    return json.dumps({
    "type": "subscribe",
    "product_ids": ["ETH-USD"],
    "channels": ["level2","heartbeat",{"name": "ticker","product_ids": ["ETH-USD"]}]
})
    
def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send(create_subscribe())
        time.sleep(1)
        print("thread terminating...")
    _thread.start_new_thread(run, ())

def request_wss():
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp("wss://ws-feed.exchange.coinbase.com",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
                
if __name__ == "__main__":
    request_wss()
    
    
    