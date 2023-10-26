from phinance.database import trades_db
from datetime import datetime
from bson.objectid import ObjectId

class TradeDB:

    def __init__(self, user_id) -> None:
        self.user_id = user_id


    def add_trade(self, asset:str, price:float, amount:float, exchange:str="Other"):
        doc = {
            "asset": asset,
            "user_id" : self.user_id,
            "currency" : "USD",
            "price" : price,
            "total_price": price*amount,
            "amount": amount,
            "status" : "active",
            "sell_price": None,
            "pnl" : None,
            "exchange": exchange,
            "trade_time" : datetime.now(),
            "updated_at" : None,
        }

        return trades_db.insert_one(doc).inserted_id


    def get_single_trade(self, trade_id:str):
        try:
            print(trade_id, self.user_id)
            trade = trades_db.find_one({"_id" : ObjectId(trade_id), "user_id": self.user_id})
            return trade
        except:
            return False


    def update_trade(self, trade_id:str, sell_price:float):
        try:
            find = trades_db.find_one_and_update(filter={"_id" : ObjectId(trade_id), "user_id": self.user_id}, update={"$set" : {"sell_price" : sell_price, "status": "closed"}}, upsert=True)
            return find
        except:
            return False


    def get_all_trades(self):
        try:
            return list(trades_db.find({"user_id": self.user_id}))
        except:
            return False


