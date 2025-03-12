from flask import Flask, render_template, request, jsonify, Response, send_file
import requests
import pandas as pd
import os
from cameratest import Camera  # Replace with your actual camera module
from flask_cors import CORS  # 允許跨域請求 (讓 GitHub Pages 可以訪問)
app = Flask(__name__, template_folder='templates')

# LINE Notify settings
LINE_NOTIFY_TOKEN = 'hY7R5E0yhqLipnfPyW7sGqCpEsLkxc6ojrb9kNbRpeV'
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/notify/feeder', methods=['POST'])
def notify():
    message = "撒餌器倒數計時已經結束！"
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
@app.route('/notify/sprayer', methods=['POST'])
def notify1():
    message = "噴灑器倒數計時已經結束！"
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

# Route for the video stream
@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

# Generator function to provide frames to the video stream
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route to download history records
@app.route('/download_history', methods=['GET'])
def download_history():
    try:
        # Make sure the file exists in the correct location
        file_path = '/home/pan/Downloads/nee/智慧捕壽籠歷史記錄.xlsx'
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({"status": "文件不存在"}), 404
    except Exception as e:
        return jsonify({"status": "無法獲取歷史紀錄", "error": str(e)}), 500

# Route to get history records (if you want to keep this functionality)
@app.route('/history', methods=['GET'])
def get_history():
    try:
        df = pd.read_excel('智慧捕壽籠歷史記錄.xlsx')  # Ensure the path is correct
        if df.empty:
            return jsonify({"status": "無歷史紀錄", "error": "Excel文件是空的"}), 404
        
        history_data = df.to_json(orient='records', force_ascii=False)  # Convert to JSON format
        return jsonify(history_data)
    except Exception as e:
        return jsonify({"status": "無法獲取歷史紀錄", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
