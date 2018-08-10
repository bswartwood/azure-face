import json
import os
import pprint

import requests

ENDPOINT_CONF = 'endpoint'
KEY_1 = 'key_1'
KEY_2 = 'key_2'

INPUT_DIR = 'images'
OUTPUT_DIR = 'results'

FACE_API_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
PARAMS = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
                            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}
IMAGE_URL = 'https://how-old.net/Images/faces2/main007.jpg'


def process_face_images(conf):
    face_conf = conf['face']
    face_endpoint = face_conf[ENDPOINT_CONF]
    face_key = face_conf[KEY_1]
    face_headers = {'Ocp-Apim-Subscription-Key': face_key,
                    'Content-Type': 'application/octet-stream'}

    # You can also hit the endpoint via image URL:
    # data = {'url': IMAGE_URL}

    for file in os.listdir(INPUT_DIR):
        with open('{}/{}'.format(INPUT_DIR, file), 'rb') as pic:
            picture = bytearray(pic.read())

        print('Processing {}'.format(file))
        response = requests.post(face_endpoint, params=PARAMS, headers=face_headers, data=picture)
        face_response_json = response.json()

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR
                        )
        with open('{}/{}.txt'.format(OUTPUT_DIR, file), 'w') as result_file:
            pprint.pprint(face_response_json, stream=result_file)


def main():
    with open('azure_keys.json', 'r') as conf:
        configuration = json.load(conf)

    process_face_images(configuration)

    return


if __name__ == '__main__':
    main()
