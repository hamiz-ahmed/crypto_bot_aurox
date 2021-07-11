
import requests
import config
import websocket, json
INITIAL_CAPITAL = 1000
import time

class BuySellCoin:
    def __init__(self):
        self.capital = INITIAL_CAPITAL
        self.coin_balance = 0
        self.transaction_fee = 0.30
        self.roi = {
        "0": 0.002,
        "90": 0.001,
        "120": 0
    }
        self.buy_price = 0
        self.buy_time = 0
        self.stoploss = -0.03
        self.sell_routine_running = False

    def get_btc_price(self, API_KEY):
        url = 'https://rest.coinapi.io/v1/exchangerate/BTC/USDT'
        headers = {'X-CoinAPI-Key': API_KEY}
        response = requests.get(url, headers=headers)

        return response.json()["rate"]
        # return 33500
    def buy_coin(self, coin_name, current_price=None):
        if coin_name=="BTC":
            if current_price:
                current_coin_price = float(current_price)
            else:
                current_coin_price = self.get_btc_price(config.BTC_PRICE_API_KEY)

            if self.capital > 0:
                self.capital = self.capital - self.transaction_fee
                self.coin_balance = self.capital / current_coin_price
                self.capital = 0
                print("\n\nBought " + coin_name + " at price: ", current_coin_price)
                print("Total coin balance is: ", self.coin_balance)
                print("Total capital is: ", self.capital)

                self.buy_price = current_coin_price
                self.buy_time = time.time()
            else:
                print("Not enough capital to buy")

    def check_for_sell(self, current_coin_price, ws):
        self.sell_routine_running = True
        minutes_since_bought = (time.time() - self.buy_time) / 60
        # minutes_since_bought = 130
        if minutes_since_bought > float(list(self.roi.keys())[0]) and minutes_since_bought < float(list(self.roi.keys())[1]):
            target_percent = self.roi[list(self.roi.keys())[0]]

        elif minutes_since_bought > float(list(self.roi.keys())[1]) and minutes_since_bought < float(list(self.roi.keys())[2]):
            target_percent = self.roi[list(self.roi.keys())[1]]

        else:
            target_percent = self.roi[list(self.roi.keys())[2]]

        target_percent = float(target_percent)
        target_selling_price = (1+target_percent) * self.buy_price

        if target_selling_price == self.buy_price:
            # adding transaction fee to seeling price
            target_selling_price = self.buy_price + self.transaction_fee

        stoploss_price = (1+self.stoploss) * self.buy_price

        print("\n\n\nBuying Price: ", self.buy_price)
        print("Current Price: ", current_coin_price)
        print("Target: ", target_selling_price)
        print("Stoploss: ", stoploss_price)


        # current_coin_price = self.get_btc_price(config.BTC_PRICE_API_KEY)
        if current_coin_price > target_selling_price or current_coin_price<stoploss_price:
            # sell the coin
            self.capital = self.coin_balance * current_coin_price
            self.capital = self.capital - self.transaction_fee
            self.coin_balance = 0
            print("\nSold " + "BTC" + " at price: ", current_coin_price)
            print("Total coin balance is: ", self.coin_balance)
            print("Total capital is: ", self.capital)

            self.buy_price = 0
            self.buy_time = 0
            self.sell_routine_running = False
            print("Closing socket..")
            ws.close()


    def sell_coin(self, coin_name):
        if coin_name=="BTC":
            current_coin_price = self.get_btc_price(config.BTC_PRICE_API_KEY)

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

        # elif signal=="short" and time_unit=="30_minute":
        #     self.sell_coin(coin)

    def get_current_balance(self):
        btc_price = self.get_btc_price(config.BTC_PRICE_API_KEY)
        portfolio_value = btc_price*self.coin_balance
        print("The current portfolio value is: "+ str(portfolio_value) + " and at current BTC price: " + str(btc_price))
        return {"portfolio_value": portfolio_value,
                "current_btc_price": btc_price,
                "current_capital": self.capital}

    def socket_conn_for_sell(self):
        def on_message(ws, message):
            json_msg = json.loads(message)
            current_price = float(json_msg["k"]["l"])
            # print("Current_price: ", current_price)
            self.check_for_sell(current_coin_price=current_price, ws=ws)

        def on_close(ws):
            print("Connection closed")

        socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
        ws = websocket.WebSocketApp(socket,
                                    on_message=on_message,
                                    on_close=on_close)
        self.sell_routine_running = True
        ws.run_forever()