import argparse, torch, os, numpy as np
from torchvision import transforms
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
from torchvision import models
from Model.ManyObjARTS.ZeroCostNas.foresight.dataset import get_cifar_dataloaders
from Model.ManyObjARTS.ZeroCostNas.foresight.models.nasbench2 import (
    get_model_from_arch_str
) 
from Model.ManyObjARTS.ZeroCostNas.foresight.weight_initializers import (
    init_net
)
from Model.ManyObjARTS.NASBench import NATS 

def predict():
    args = argparse.Namespace(api_loc='', 
                            outdir='',
                            init_w_type='none', # Initialize weight
                            init_b_type='none', # Initialize bias
                            batch_size=256,      # Batch size
                            dataset='cifar10',
                            gpu=0,
                            num_data_workers=0,
                            dataload='random',
                            dataload_info=1,
                            seed=2,
                            write_freq=1,
                            start=0,
                            end=0,
                            noacc=False,
                            index_arch = [1, 3, 0, 1, 0, 2]
                            )

    api = NATS.NATS(debug=True)
    api.device = 'cpu'
    arch_str = api.convert_individual_to_query(ind=args.index_arch)

    cell = models.vgg16(pretrained=True)
    net = cell.to(api.device)
    print(cell)
    input_lastLayer = net.classifier[6].in_features
    net.classifier[6] = torch.nn.Linear(input_lastLayer, 10)
    
    if api.device == 'cpu':
        net.load_state_dict(torch.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'best_model.pt'), map_location=torch.device('cpu')))
    else:
        net.load_state_dict(torch.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'best_model.pt')))
        
    mean = (0.4914, 0.4822, 0.4465)
    std = (0.2023, 0.1994, 0.2010)
    size, pad = 32, 4

    test_transform = {
        'demo': transforms.Compose([
                        transforms.Resize(size),
                        transforms.ToTensor(),
                        transforms.Normalize(mean,std),
                    ])    
    }

    data_dir = os.path.dirname(os.path.realpath(__file__))
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x), test_transform[x])
                    for x in ['demo']}
    data_loader = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=args.batch_size, shuffle=True, num_workers=args.num_data_workers)
                    for x in ['demo']}

    net.eval()

    truth_label = {
        0: 'airplane',
        1: 'automobile',
        2: 'frog',
        3: 'cat',
        4: 'horse',
        5: 'dog',
        6: 'bird',
        7: 'deer',
        8: 'ship',
        9: 'truck'
    }
    prediction = None
    probability = None
    print("Model predict:", end =' ')
    for inputs, _ in data_loader['demo']:
        inputs = inputs.to(api.device)
        out = net(inputs)  
        _, preds = torch.max(out, 1)
        probability = torch.nn.Softmax(dim=1)(out)
        print(probability)
        print(int(np.squeeze(preds.cpu().numpy().T)))
        prob = round(np.max(probability.detach().numpy()[0])  * 100, 2)
        print(prob)
        prediction = truth_label[int(np.squeeze(preds.cpu().numpy().T))]
        print(f"{prediction}, {prob}")
    return prediction, prob