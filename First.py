# -*- coding: utf-8 -*-

import requests
import websockets
import json

class CoinbaseObj():
    
    URL = "https://api-public.sandbox.pro.coinbase.com/products/BTC-USD/book"
    
    def __init__(self, product_id):
        self.product_id = product_id
        self.result_request = dict()
        
    #@classmethod
    def change_URL(self):
        new_URL = self.URL.split("/")
        new_URL[4]=self.product_id
        new_URL = "/".join(new_URL)
        return new_URL
    
    def getOrderBook(self):
        self.result_request = requests.get(self.change_URL()).json()
        print(self.result_request)
        return self.result_request

if __name__ == "__main__":
    obj = CoinbaseObj("BTC-USD")
    result = obj.getOrderBook()
    test = obj.change_URL()
