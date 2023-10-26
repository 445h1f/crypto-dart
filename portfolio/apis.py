import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

CMC_API_KEY = os.getenv('CMC_API_KEY')
CRYPTO_NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class CMCApi:
    __BASE_URI = 'https://pro-api.coinmarketcap.com/'
    __SYMBOLS_LIST = ['BTC', 'ETH', 'BNB', 'XRP', 'SOL', 'LINK', 'ADA', 'DOGE', 'TRX', 'LTC', 'MATIC', 'BCH', 'AVAX', 'ICP', 'STX', 'APE']

    __HEADERS = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_API_KEY
    }

    def get_coins_prices(self, symbols:list=None):
        url = self.__BASE_URI + 'v2/cryptocurrency/quotes/latest'

        if symbols is None:
            symbols = self.__SYMBOLS_LIST

        symbols = ','.join(symbols)

        params = {
            "symbol" : symbols,
            "convert" : "USD"
        }

        r = requests.get(url, params=params, headers=self.__HEADERS)
        data = {}
        try:
            json_response = r.json()["data"]

            for key in json_response:
                data[key] = json_response[key][0]["quote"]["USD"]

            return data
        except:
            return {}





def get_crypto_news(asset:str=None):
    url = f'https://newsdata.io/api/1/news?apikey={CRYPTO_NEWS_API_KEY}&q='
    if asset is None:
        asset = ['BITCOIN', 'ETHEREUM', 'BINANCE COIN', 'RIPPLE', 'SOLANA', 'CHAINLINK', 'CARDANO', 'DOGECOIN', 'TRON', 'CHAINLINK', 'LITECOIN', 'POLYGON', 'BITCOIN CASH', 'AVALANCE', 'INTERENT COMPUTER', 'STACKS', 'APE COIN']

    asset_q = ' OR '.join(asset)
    q = f"crypto AND ({asset_q})"
    url += q

    r = requests.get(url)

    if r.status_code == 200:
        return r.json()
    else:
        return False




