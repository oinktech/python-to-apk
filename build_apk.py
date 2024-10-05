import sys
import os
import shutil
import subprocess

def main():
    # 獲取上傳的文件路徑
    if len(sys.argv) < 2:
        print("請提供要打包的 Python 程式碼包路徑")
        return

    file_path = sys.argv[1]
    buildozer_folder = "buildozer"

    if os.path.exists(buildozer_folder):
        shutil.rmtree(buildozer_folder)
    os.makedirs(buildozer_folder)

    # 解壓上傳的文件
    try:
        shutil.unpack_archive(file_path, buildozer_folder)
    except Exception as e:
        print(f"解壓失敗: {e}")
        return

    os.chdir(buildozer_folder)

    # 初始化 Buildozer 配置
    try:
        subprocess.run(["buildozer", "init"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Buildozer 初始化失敗: {e}")
        return

    # 開始打包 APK
    try:
        print("開始打包 APK，請稍候...")
        process = subprocess.run(["buildozer", "android", "debug"], check=True)

        if process.returncode == 0:
            print("APK 打包成功！")
            print("APK 文件位於：bin/")
        else:
            print("APK 打包失敗，請檢查錯誤信息。")
    except subprocess.CalledProcessError as e:
        print(f"打包過程中發生錯誤: {e}")

if __name__ == '__main__':
    main()
