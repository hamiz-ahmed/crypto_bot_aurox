from flask import Flask, request, Response
from logic import BuySellCoin
app = Flask(__name__)


btc = BuySellCoin()
# eth = BuySellCoin()
@app.route('/webhook', methods=['POST'])
def respond():
    # print(request.json)
    # print(request.json["test"])
    btc.read_signal(response_json=request)
    return Response(status=200)


if __name__=="__main__":

    app.run()