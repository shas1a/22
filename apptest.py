from flask import Flask, render_template, request, jsonify, Response, send_file, redirect
import requests
import os
from flask_cors import CORS  # 允許跨域請求 (讓 GitHub Pages 可以訪問)
from cameratest import Camera  # 確保你的 camera 模組存在

app = Flask(__name__, template_folder='templates')
CORS(app)  # 啟用 CORS，允許來自 GitHub Pages 的請求

# LINE Notify 設定
LINE_NOTIFY_TOKEN = 'hY7R5E0yhqLipnfPyW7sGqCpEsLkxc6ojrb9kNbRpeV'
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'

@app.route('/')
def index():
    return render_template('index.html')

# 通知撒餌器
@app.route('/notify/feeder', methods=['POST'])
def notify():
    return send_line_notify("撒餌器倒數計時已經結束！")

# 通知噴灑器
@app.route('/notify/sprayer', methods=['POST'])
def notify1():
    return send_line_notify("噴灑器倒數計時已經結束！")

def send_line_notify(message):
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {'message': message}
    try:
        response = requests.post(LINE_NOTIFY_URL, headers=headers, data=data)
        if response.status_code == 200:
            return jsonify({"status": "通知已發送"})
        else:
            return jsonify({"status": "通知發送失敗", "error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"status": "通知發送失敗", "error": str(e)}), 500

# 影片串流
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# **下載歷史紀錄 Excel (從 Google Sheets 下載)**
@app.route('/download_history', methods=['GET'])
def download_history():
    # Google Sheets 下載連結
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1N4wr5UvIzRoUJ9z1hoGaZ4DLkln8jEh4/export?format=xlsx"
    return redirect(GOOGLE_SHEETS_URL)

# **取得歷史紀錄 JSON**
@app.route('/history', methods=['GET'])
def get_history():
    try:
        # 這裡改為不再從本地檔案獲取，因為我們現在用 Google Sheets
        # file_path = 'conchhistory.xlsx'
        # if not os.path.exists(file_path):
        #     return jsonify({"status": "無歷史紀錄", "error": "文件不存在"}), 404

        # df = pd.read_excel(file_path)
        # if df.empty:
        #     return jsonify({"status": "無歷史紀錄", "error": "Excel文件是空的"}), 404

        # history_data = df.to_json(orient='records', force_ascii=False)
        # return jsonify(history_data)

        return jsonify({"status": "使用 Google Sheets 直接下載 Excel"}), 200
    except Exception as e:
        return jsonify({"status": "無法獲取歷史紀錄", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
