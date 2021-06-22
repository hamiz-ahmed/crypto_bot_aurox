from flask import Flask, request, Response
from logic import BuySellCoin
app = Flask(__name__)


bs = BuySellCoin()

@app.route('/webhook', methods=['POST'])
def respond():
    print(request.json)
    # print(request.json["test"])
    bs.read_signal(response_json=request)
    return Response(status=200)


if __name__=="__main__":

    app.run()