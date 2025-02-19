import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    redirect
)

from src.analyze_faces import analyze_face
from src.emotions import translate_emotions

app = Flask(__name__, template_folder='src/templates')

UPLOAD_FOLDER = './static/uploaded_images'
PROCESSED_FOLDER = './static/processed_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

users = {
    'admin': 'password'
}

@app.route("/")
def index():
    return render_template('login.html')

@app.route('/home', methods=['POST'])
def return_to_home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        return redirect(url_for('after_login'))
    else:
        return render_template('loginFail.html')

@app.route('/top', methods=['GET'])
def after_login():
    return render_template('imageUpload.html')

# ファイルを受け取る方法の指定
@app.route('/upload-image', methods=['GET', 'POST'])
def process_uploaded_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # 元画像を保存
    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_path)

    output_path = os.path.join(PROCESSED_FOLDER, file.filename)
    image, emotion_raw_list = analyze_face(input_path, output_path)
    image.save(output_path)

    emotions = translate_emotions(emotion_raw_list)

    img_url = f"processed_images/{file.filename}"
    return render_template('imageUploaded.html', img_url = img_url, emotions = emotions)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # 環境変数PORTがない場合はデフォルト5000
    app.run(host="0.0.0.0", port=port)