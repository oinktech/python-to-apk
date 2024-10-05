from flask import Flask, render_template, request, redirect, url_for, flash
import os
import subprocess
import shutil

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於顯示 Flash 消息
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('沒有檔案被上傳！')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('檔案名稱無效！')
        return redirect(request.url)

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        flash('檔案上傳成功！開始打包 APK...')
        
        # 調用打包腳本
        build_process = subprocess.run(['python3', 'build_apk.py', file_path], capture_output=True, text=True)

        if build_process.returncode == 0:
            flash('APK 打包成功！')
            return redirect(url_for('result', success=True))
        else:
            flash('APK 打包失敗，請檢查錯誤信息。')
            return redirect(url_for('result', success=False))

@app.route('/result')
def result():
    success = request.args.get('success', 'false') == 'true'
    return render_template('result.html', success=success)

if __name__ == '__main__':
    app.run(debug=True,port=10000, host='0.0.0.0')
