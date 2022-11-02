import io
import os
from google.cloud import vision
#
# def main():
#

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/leedongseop/googleAPIjson/shorttrack-ocr-c1a61c47c944.json"
client = vision.ImageAnnotatorClient()

path = '/Users/leedongseop/PycharmProjects/tello/photo/img.png'
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations
content = texts[0].description
content = content.replace(',', '')
print(content)
#
#     return content
#
# if __name__ == "__main__":
#     main()