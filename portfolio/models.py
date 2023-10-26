from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Asset(models.Model):
#     name = models.CharField(max_length=50)
#     symbol = models.CharField(max_length=10)



BUY_CHOICES = [
    ("BTC", "BITCOIN"),
    ("ETH", "ETHEREUM"),
    ("BNB", "BINANCE COIN"),
    ("XRP", "RIPPLE"),
    ("SOL", "SOLANA"),
    ("LINK", "CHAINLINK"),
    ("ADA", "CARDANO"),
    ("DOGE", "DOGECOIN"),
    ("TRX", "TRON"),
    ("LINK", "CHAINLINK"),
    ("LTC", "LITECOIN"),
    ("MATIC", "POLYGON"),
    ("BCH", "BITCOIN CASH"),
    ("AVAX", "AVALANCE"),
    ("ICP", "INTERENT COMPUTER"),
    ("STX", "STACKS"),
    ("APE", "APE COIN"),
]

# # SELL_CHOICES = [
# #     ("USDT", "TETHER"),
# # ]

# # data model for trade
# class Trade(models.Model):
#     #list of
#     user = models.ForeignKey(to=User, on_delete=models.CASCADE)
#     asset_bought = models.ForeignKey(to=Asset)
#     asset_sold = models.ForeignKey(to=Asset)
#     price = models.FloatField() # price at which asset is bought
#     amount = models.FloatField() # amount of bought asset
#     fees = models.FloatField() # fees in tx
#     platform = models.CharField(max_length=50) # platform where trade happened
#     time = models.TimeField() # time of trade
#     thought_sell_price = models.FloatField(default=None) # profit price user thought

#     def __str__(self) -> str:
#         return f'{self.asset_bought}/{self.asset_sold}'
