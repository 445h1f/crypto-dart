from django.shortcuts import render, redirect
from .db import TradeDB
from django.contrib import messages
from .apis import CMCApi, get_crypto_news
import random
# Create your views here.

# def portfolio(request):
#     return render()

cmc = CMCApi()


ASSETS = {
    "BTC" : "BITCOIN",
    "ETH" : "ETHEREUM",
    "BNB" : "BINANCE COIN",
    "XRP" : "RIPPLE",
    "SOL" : "SOLANA",
    "LINK" : "CHAINLINK",
    "ADA" : "CARDANO",
    "DOGE" : "DOGECOIN",
    "TRX" : "TRON",
    "LINK" : "CHAINLINK",
    "LTC" : "LITECOIN",
    "MATIC" : "POLYGON",
    "BCH" : "BITCOIN CASH",
    "SHIB" : "SHIB INU",
    "AVAX" : "AVALANCE",
    "ICP" : "INTERENT COMPUTER",
    "STX" : "STACKS",
    "APE" : "APE COIN",
    "PEPE" : "PEPE COIN"
}

EXCHANGES = ['BINANCE', 'BITFINEX', 'BITGET', 'BYBIT', 'COINBASE', 'KRAKEN', 'KUCOIN', 'MEXC', 'OKX', 'OTHER']

def add_trade(request):
    context = {
        "assets" : [{"symbol" : i, "name": ASSETS[i]} for i in ASSETS],
        "exchange" : EXCHANGES,
        "title": "Add Trade"
    }

    if request.method == 'POST':
        tdb = TradeDB(request.user.username)

        asset = request.POST["asset"]
        if asset.upper() not in ASSETS:
            messages.error(request, "Invalid asset")
            return redirect('add_trade')

        exchange = request.POST["exchange"]

        try:
            price = float(request.POST["price"])
            amount = float(request.POST["amount"])
        except:
            messages.error(request, "Enter numbers only.")
            return redirect('add_trade')


        # print(asset, currency, price, amount, platform, tax, target_price, trade_time)
        tdb.add_trade(asset=asset, price=price, amount=amount, exchange=exchange)

        messages.success(request, "Trade saved successfully.")
        return redirect('view_all_trades')

    return render(request, 'portfolio/add_trade.html', context=context)


def view_all_trades(request):
    tradesObj = TradeDB(request.user.username)
    all_trades = tradesObj.get_all_trades()

    if all_trades:
        symbols = []

        live_price = cmc.get_coins_prices()

        for trade in all_trades:
            asset = trade["asset"]
            if asset in live_price:
                current_price = live_price[asset]['price']

                current_total = trade["amount"] * current_price - trade["amount"] * trade["price"]
                # if current_price < trade["price"]:
                trade["pnl"] = round(current_total, 2)
    else:
        all_trades = []


    context = {
        "trades" : all_trades,
        "title": "All Trades"
    }

    return render(request, 'portfolio/all_trades.html', context=context)


def close_trade(request, trade_id):
    # trade_data = {}
    tradeObj = TradeDB(request.user.username)
    trade = tradeObj.get_single_trade(trade_id)

    if request.method == 'POST':
        if trade:
            try:
                close_price = float(request.POST["close_price"])

                if close_price <= 0:
                    raise Exception("Close price must be greater than 0.")
            except:
                messages.error(request, "Invalid close price.")

            trade = tradeObj.update_trade(trade_id=trade_id, sell_price=close_price)
        elif trade["status"] == "closed":
            messages.error("trade is already closed")

        else:
            messages.error("trade not found.")

        return redirect('view_all_trades')


    context = {
        "trade": trade,
        "title": "Trade View"
    }

    if trade:
        if trade["status"] == "active":
            live_price = cmc.get_coins_prices()
            asset = trade['asset']
            if asset in live_price:
                current_price = live_price[asset]['price']
                trade["current_price"] = current_price
                current_total = trade["amount"] * current_price - trade["amount"] * trade["price"]
                # if current_price < trade["price"]:
                trade["pnl"] = round(current_total, 2)
            else:
                trade["pnl"] = "error"
        else:
            trade["pnl"] = trade["amount"] * trade["sell_price"] - trade["amount"] * trade["price"]


    return render(request, 'portfolio/single_trade.html', context)


def dashboard(request):
    context = {}

    tradeObj = TradeDB(request.user.username)
    assets = {}
    exchanges = {}
    all_trades = tradeObj.get_all_trades()

    live_price = cmc.get_coins_prices()
    if all_trades:
        for trade in all_trades:
            asset = trade["asset"]
            current_price = live_price[asset]["price"]
            if asset not in assets:
                assets[asset] = {
                    "current_price": current_price,
                    "total_quantity" : trade["amount"],
                    "total_buy_price" : trade["price"],
                    "active_investment" : 0,
                    "closed_investment": 0,
                    "avg_price" : 0,
                    "pnl" : 0,
                    "count": 1,
                }

                if trade["status"] == "active":
                    assets[asset]["active_investment"] = trade["amount"] * trade["price"]
                    assets[asset]["pnl"] = trade["amount"] * current_price - trade["amount"] * trade["price"]
                else:
                    assets[asset]["closed_investment"] = trade["amount"] * trade["price"]
                    assets[asset]["pnl"] = trade["amount"] * trade["sell_price"] - trade["amount"] * trade["price"]
                assets[asset]["avg_price"] = trade["price"]
            else:
                assets[asset]["count"] += 1
                assets[asset]["total_quantity"] += trade["amount"]

                if trade["status"] == "active":
                    assets[asset]["active_investment"] += trade["amount"] * trade["price"]
                    assets[asset]["pnl"] += trade["amount"] * current_price - trade["amount"] * trade["price"]
                else:
                    assets[asset]["closed_investment"] += trade["amount"] * trade["price"]
                    assets[asset]["pnl"] += trade["amount"] * trade["sell_price"] - trade["amount"] * trade["price"]
                assets[asset]["avg_price"] = trade["price"]

                assets[asset]["avg_price"] = (assets[asset]["avg_price"] + trade["price"]) / assets[asset]["count"]

        x = []
        for k, v in assets.items():
            v["name"] = k;

            for i in v:
                if isinstance(v[i], float):
                    v[i] = round(v[i], 3)
            x.append(v)
    else:
        x = []

    context = {
        "assets" : x,
        "title" : "Dashboard"
    }

    return render(request, 'portfolio/dashboard.html', context)



def view_news(request):
    news = get_crypto_news()

    if news:
        news_list = news["results"]
    else:
        news_list = []

    img = ['news.jpeg', 'news2.jpeg', 'news3.jpeg', 'news4.jpg', 'news5.jpg']
    context = {
        "title" : "Crypto News",
        "news_list" : news_list,
        "random_images" : img
    }
    return render(request, 'portfolio/news.html', context=context)