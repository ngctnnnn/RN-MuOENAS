pip install -q ConfigSpace pathvalidate
pip install -q torch-scatter torch-sparse torch-cluster torch-spline-conv torch-geometric -f https://data.pyg.org/whl/torch-1.10.0+cu102.html
pip install -q torch==1.10.0+cu102 torchvision==0.11.1+cu102 torchaudio===0.10.0+cu102 -f https://download.pytorch.org/whl/cu102/torch_stable.html
git clone https://github.com/automl/nasbench301
pip install -q nasbench301
pip install -q xgboost==1.4.0
pip install -q graphviz