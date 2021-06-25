
import requests


INITIAL_CAPITAL = 1000
BTC_PRICE_API_KEY = '2AC15ABF-77EA-4158-84BA-5B781B29EDD2'

class BuySellCoin:
    def __init__(self):
        self.capital = INITIAL_CAPITAL
        self.coin_balance = 0
        self.transaction_fee = 0.30

    def get_btc_price(self, API_KEY):
        url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USDT'
        headers = {'X-CoinAPI-Key': API_KEY}
        response = requests.get(url, headers=headers)

        return response.json()["rate"]

    def buy_coin(self, coin_name, current_price=None):
        if coin_name=="BTC":
            if current_price:
                current_coin_price = float(current_price)
            else:
                current_coin_price = self.get_btc_price(BTC_PRICE_API_KEY)

            if self.capital > 0:
                self.capital = self.capital - self.transaction_fee
                self.coin_balance = self.capital / current_coin_price
                self.capital = 0
                print("\n\nBought " + coin_name + " at price: ", current_coin_price)
                print("Total coin balance is: ", self.coin_balance)
                print("Total capital is: ", self.capital)
            else:
                print("Not enough capital to buy")

    def sell_coin(self, coin_name):
        if coin_name=="BTC":
            current_coin_price = self.get_btc_price(BTC_PRICE_API_KEY)

            if self.coin_balance > 0:
                self.capital = self.coin_balance * current_coin_price
                self.capital = self.capital - self.transaction_fee
                self.coin_balance = 0
                print("\nSold " + coin_name + " at price: ", current_coin_price)
                print("Total coin balance is: ", self.coin_balance)
                print("Total capital is: ", self.capital)
            else:
                print("Not enough balance to sell..")

    def read_signal(self, response_json):

        time_unit = response_json.json["timeUnit"]
        coin = response_json.json["base"]
        is_confirmed = response_json.json["confirmed"]
        signal = response_json.json["signal"]
        current_coin_price = None
        if "current_price" in response_json.json:
            current_coin_price = response_json.json["current_price"]

        if coin == "BTC":
            print(response_json)

        if signal == "long" and time_unit=="30_minute":
            self.buy_coin(coin, current_coin_price)
        elif signal=="short" and time_unit=="30_minute":
            self.sell_coin(coin)

    def get_current_balance(self):
        btc_price = self.get_btc_price(BTC_PRICE_API_KEY)
        portfolio_value = btc_price*self.coin_balance
        print("The current portfolio value is: "+ str(portfolio_value) + " and at current BTC price: " + str(btc_price))
        return {"portfolio_value": portfolio_value,
                "current_btc_price": btc_price}