from flask import Flask
from flask import request
from nsfw_detector import predict
import requests
import random
import string
import shutil 
import os
import time
import urllib.request
import zipfile
import gc

import tensorflow as tf
from private_detector.private_detector.utils.preprocess import preprocess_for_evaluation

app = Flask(__name__)

MODEL_PATH = 'mobilenet_v2_140_224'
letters = string.ascii_lowercase

def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        zf.extractall(dest_dir)

def fetch_private_detector_model():
  target = '_private_detector_saved_model/private_detector/saved_model'
  if os.path.exists(target):
    print('using cache')
    return target
  zip_dir = '_private_detector_saved_model'
  url = 'https://storage.googleapis.com/private_detector/private_detector.zip'
  filehandle, _ = urllib.request.urlretrieve(url)
  unzip(filehandle, zip_dir)
  return target

private_detector_path = fetch_private_detector_model()
del fetch_private_detector_model
del unzip
gc.collect()

model_v2 = tf.saved_model.load(private_detector_path)
model = predict.load_model(MODEL_PATH)

def download_image(url, dest):
    r = requests.get(url, stream = True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
        
        # Open a local file with wb ( write binary ) permission.
        with open(dest,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return True
    return False

def read_image(url: str) -> tf.Tensor:
    """
    Load and preprocess image for inference with the Private Detector

    Parameters
    ----------
    filename : str
        Filename of image

    Returns
    -------
    image : tf.Tensor
        Image ready for inference
    """
    image = tf.io.decode_jpeg(requests.get(url).content, channels=3)

    image = preprocess_for_evaluation(
        image,
        480,
        tf.float16
    )

    image = tf.reshape(image, -1)

    return image

@app.route('/health', methods=['GET'])
def health():
  return {'status': 'ok'}

@app.route('/predict', methods=['POST'])
def upload():
    file_path = ''.join(random.choice(letters) for i in range(10))
    download_image(request.args.get('url'),file_path)
    res = predict.classify(model, file_path, predict.IMAGE_DIM)
    os.remove(file_path) 

    # Call the prediction function
    return res[file_path]

@app.route('/models/private_detector/predict', methods=['POST'])
def predictV2():
    t0 = time.time()
    url = request.args.get('url')
    image = read_image(url)
    preds = model_v2([image])

    # Call the prediction function
    return { 'private_detector': preds.numpy().tolist()[0][0], 'time': (time.time() - t0) }

@app.route('/models/all/predict', methods=['POST'])
def predictV2():
    t0 = time.time()
    url = request.args.get('url')
    image = read_image(url)
    preds = model_v2([image])

    file_path = ''.join(random.choice(letters) for i in range(10))
    download_image(url, file_path)
    res = predict.classify(model, file_path, predict.IMAGE_DIM)
    os.remove(file_path) 

    # Call the prediction function
    return { 'private_detector': preds.numpy().tolist()[0][0], 'time': (time.time() - t0), 'nsfw_model': res[file_path] }


if __name__ == '__main__':
    app.run(debug=True)
