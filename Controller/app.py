import time
from flask import Flask, jsonify, redirect, request
from Model.inference import predict
from werkzeug.utils import secure_filename
import os
import cv2
print()
os.system(f"cd {__file__[:-len('app.py')]} && clear")
# if 'BE' in os.system('ls'):
#     os.system('cd BE && clear')
# else:
#     os.system('clear')
app = Flask(__name__)
app.config['files'] = os.path.join(__file__[:-len('app.py')], 'demo/demo')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(file):
    if file.filename[-4] in ALLOWED_EXTENSIONS: return True
    else: return False

@app.route("/image", methods=['GET', 'POST'])
def image():
    if(request.method == "POST"):
        bytesOfImage = request.get_data()
        with open('./Model/demo/demo/1.png', 'wb') as out:
            if bytesOfImage == None:
                raise Exception('Image not found')
            out.write(bytesOfImage)
        print('Original img: ',end='')
        print(cv2.imread('./Model/demo/demo/1.png').shape)
        time.sleep(1)
        # try:
        prediction, probability = predict()
        return {'Prediction': prediction, "Probability": str(probability)+"%"}
        # except:
        #     return "Error while processing"

if __name__ == "__main__":
    app.run(debug=True)