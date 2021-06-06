from flask import Flask
from flask import request
# from nsfw_detector import predict
import requests
import random
import string
import shutil 
import os

app = Flask(__name__)

MODEL_PATH = 'mobilenet_v2_140_224'
letters = string.ascii_lowercase

# model = predict.load_model(MODEL_PATH)    

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

@app.route('/health', methods=['GET'])
def health():
  return {'status': 'ok'}

@app.route('/predict', methods=['POST'])
def upload():
    file_path = ''.join(random.choice(letters) for i in range(10))
    download_image(request.args.get('url'),file_path)
    # res = predict.classify(model, file_path, predict.IMAGE_DIM)
    os.remove(file_path) 

    # Call the prediction function
    return res[file_path]


if __name__ == '__main__':
    app.run(debug=True)
