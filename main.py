from flask import Flask, request, Response
from logic import BuySellCoin
from flask import jsonify
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


if __name__=="__main__":
    app.run()