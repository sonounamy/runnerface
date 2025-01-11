import boto3
import base64
import io
import uuid

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

S3_BUCKET_NAME = 'runnerface-image'

def lambda_handler(event, context):
    # Base64形式の画像データを取得
    image_data = base64.b64decode(event['body'])

    # 元の画像をS3にアップロード
    original_image_key = f"original_images/{uuid.uuid4()}.jpg"
    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=original_image_key,
        Body=image_data,
        ContentType='image/jpeg'
    )

    # Rekognitionで顔検出
    response = rekognition.detect_faces(
        Image={'Bytes': image_data},
        Attributes=['ALL']
    )

    # 顔検出の結果を返却
    faces = response['FaceDetails']
    face_bounding_boxes = []
    for face in faces:
        face_bounding_boxes.append(face['BoundingBox'])

    # 結果を返却
    return {
        'statusCode': 200,
        'body': {
            'original_image_url': f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{original_image_key}",
            'faces_bounding_boxes': face_bounding_boxes
        }
    }
