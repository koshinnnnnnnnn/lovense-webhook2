import requests
from flask import Flask, request, jsonify

# Flaskサーバーを立ち上げる
app = Flask(__name__)

# Lovense APIの設定（スマホのIPアドレスを指定）
LOVENSE_IP = "192.168.0.7"  # ← スマホのIPアドレスに変更
PORT = "20010"

# Lovenseの操作関数
def control_lovense(command):
    if command == "ミオ強くして":
        url = f"http://{LOVENSE_IP}:{PORT}/V2/Vibrate?v=10&t=20"
    elif command == "ミオ止めて":
        url = f"http://{LOVENSE_IP}:{PORT}/V2/Stop"
    elif command == "ミオ優しくして":
        url = f"http://{LOVENSE_IP}:{PORT}/V2/Vibrate?v=3&t=20"
    elif command == "ミオランダム":
        url = f"http://{LOVENSE_IP}:{PORT}/V2/Pattern?name=wave&t=30"
    else:
        return "無効なコマンド"

    response = requests.get(url)
    return "実行しました" if response.status_code == 200 else "エラーが発生しました"

# Webhookエンドポイント（チャットのメッセージを受信）
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        command = data["message"]
        result = control_lovense(command)
        return jsonify({"status": result})
    return jsonify({"status": "無効なリクエスト"})

# Flaskサーバーを起動
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
