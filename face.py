'''
Face API Docs:
https://westcentralus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236

Vision API Docs:
https://westus.dev.cognitive.microsoft.com/docs/services/56f91f2d778daf23d8ec6739/operations/56f91f2e778daf14a499e1fa
'''

import json
import os
import pprint

import requests

ENDPOINT_CONF = 'endpoint'
KEY_1 = 'key_1'
KEY_2 = 'key_2'

INPUT_DIR = 'images'
FACE_OUTPUT_DIR = 'face_results'
VISION_OUTPUT_DIR = 'vision_results'

FACE_API_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
FACE_PARAMS = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
                            'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}

VISION_PARAMS = {'visualFeatures': 'Tags, Color, Categories, Description, Faces'}
IMAGE_URL = 'https://how-old.net/Images/faces2/main007.jpg'


def process_images(input_dir, output_dir, endpoint, headers, params):
    for file in os.listdir(input_dir):
        with open('{}/{}'.format(input_dir, file), 'rb') as pic:
            picture = bytearray(pic.read())

        print('Processing {} using {}'.format(file, endpoint))
        response = requests.post(endpoint, params=params, headers=headers, data=picture)
        face_response_json = response.json()

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        result_path = '{}/{}.txt'.format(output_dir, file)
        print('Writing results to {}'.format(result_path))
        with open(result_path, 'w') as result_file:
            pprint.pprint(face_response_json, stream=result_file)


def process_face_images(conf):
    face_endpoint = conf[ENDPOINT_CONF]
    face_key = conf[KEY_1]
    face_headers = {'Ocp-Apim-Subscription-Key': face_key,
                    'Content-Type': 'application/octet-stream'}

    # You can also hit the endpoint via image URL:
    # data = {'url': IMAGE_URL}

    process_images(INPUT_DIR, FACE_OUTPUT_DIR, face_endpoint, face_headers, FACE_PARAMS)


def process_vision_images(conf):
    vision_endpoint = conf[ENDPOINT_CONF]
    vision_key = conf[KEY_1]
    vision_headers = {'Ocp-Apim-Subscription-Key': vision_key,
                      'Content-Type': 'application/octet-stream'}
    process_images(INPUT_DIR, VISION_OUTPUT_DIR, vision_endpoint, vision_headers, VISION_PARAMS)


def main():
    with open('azure_keys.json', 'r') as conf:
        configuration = json.load(conf)

    process_face_images(configuration['face'])
    process_vision_images(configuration['vision'])

    return


if __name__ == '__main__':
    main()
