import base64
import requests

from src.draw_bounding_boxes import draw_bounding_boxes

API_URL = "https://2p2dwmmqca.execute-api.ap-northeast-1.amazonaws.com/runnerface-dev/upload"

def send_image_to_api(image_path, api_url):
    # 画像を読み込んでBase64エンコード
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # リクエストペイロードを作成
    payload = {
        "body": base64_image
    }

    # ヘッダーを設定
    headers = {
        "Content-Type": "application/json"
    }

    # POSTリクエストを送信
    response = requests.post(api_url, json=payload, headers=headers)

    # レスポンスを表示
    try:
        response_dict = response.json()
    except ValueError:
        raise Exception("terminated")
    
    return response_dict["body"]["results"]


def analyze_face(input_path, output_path):
    runner_face_data = send_image_to_api(input_path, API_URL)
    image = draw_bounding_boxes(
        image_path=input_path,
        faces=runner_face_data
    )
    return image, [item["Emotions"] for item in runner_face_data]
