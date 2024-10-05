from flask import Flask, request, redirect, url_for, render_template, send_from_directory, flash, jsonify
import os
import subprocess
from werkzeug.utils import secure_filename
import shutil
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 設定一個秘密金鑰以支持 session

# 上傳文件的文件夾
UPLOAD_FOLDER = 'uploads'
BUILDOZER_FOLDER = 'buildozer'
ALLOWED_EXTENSIONS = {'zip', 'tar', 'gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['BUILDOZER_FOLDER'] = BUILDOZER_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BUILDOZER_FOLDER, exist_ok=True)

def allowed_file(filename):
    """判斷文件是否允許的類型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """主頁面"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """處理文件上傳"""
    if 'file' not in request.files:
        flash('沒有選擇文件，請重新上傳')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('請選擇一個文件')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('文件成功上傳，正在打包 APK...')

        # 启动打包进程（异步）
        subprocess.Popen(['python', 'build_apk.py', file_path], shell=False)

        return redirect(url_for('progress'))

    flash('支持的文件類型：zip, tar, gz')
    return redirect(request.url)

@app.route('/progress')
def progress():
    """打包進度頁面"""
    return render_template('progress.html')

@app.route('/status')
def status():
    """返回打包進度狀態，模擬進度條"""
    # 假设你记录打包状态，返回进度
    return jsonify({'status': '打包中...', 'progress': 50})

@app.route('/download/<filename>')
def download_file(filename):
    """允許下載打包好的 APK 文件"""
    return send_from_directory(app.config['BUILDOZER_FOLDER'], filename)

def build_apk(file_path):
    """處理 APK 打包過程"""
    try:
        shutil.unpack_archive(file_path, app.config['BUILDOZER_FOLDER'])
        subprocess.run(['buildozer', '-v', 'android', 'debug'], cwd=app.config['BUILDOZER_FOLDER'], check=True)
        flash('APK 打包完成！可下載您的 APK 文件。')
    except subprocess.CalledProcessError as e:
        flash(f'打包失敗: {e}')
    except Exception as e:
        flash(f'發生錯誤: {e}')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=10000)
