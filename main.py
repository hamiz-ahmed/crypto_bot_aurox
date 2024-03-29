from flask import Flask, request, Response, after_this_request
from logic import BuySellCoin
from flask import jsonify


# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor


app = Flask(__name__)


btc = BuySellCoin()
# eth = BuySellCoin()
@app.route('/webhook', methods=['POST'])
def respond():
    # print(request.json)
    # print(request.json["test"])
    btc.read_signal(response_json=request)


    return Response(status=200)


@app.route('/get_balance', methods=['GET'])
def get_balance():
    balance_dict = btc.get_current_balance()
    return jsonify(balance_dict)




# @app.route('/socket', methods=['GET'])
# def socket_conn():
#     def on_message(ws, message):
#         print(message)
#         return Response(status=200)
#
#     def on_close(ws):
#         print("Connection closed")
#
#     socket = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
#     ws = websocket.WebSocketApp(socket,
#                                 on_message=on_message,
#                                 on_close=on_close)
#     ws.run_forever()







if __name__=="__main__":
    app.run()