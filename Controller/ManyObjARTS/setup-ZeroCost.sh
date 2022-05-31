#!/bin/sh
pip install -q torch==1.10 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
pip install -q torchtext==0.9.1
pip install -q onnx