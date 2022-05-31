from torch.utils.data import DataLoader
from torchvision.datasets import MNIST, CIFAR10, CIFAR100, SVHN
from torchvision.transforms import Compose, ToTensor, Normalize
from torchvision import transforms
import re 

from .imagenet16 import *


def get_cifar_dataloaders(train_batch_size, test_batch_size, dataset, num_workers, resize=None, datadir='_dataset', valid_split=0):

    if valid_split > 0:
        valid_batch_size = train_batch_size

    if 'ImageNet16' in dataset:
        mean = [x / 255 for x in [122.68, 116.66, 104.01]]
        std  = [x / 255 for x in [63.22,  61.26 , 65.09]]
        size, pad = 16, 2
    elif 'cifar' in dataset:
        mean = (0.4914, 0.4822, 0.4465)
        std = (0.2023, 0.1994, 0.2010)
        size, pad = 32, 4
    elif 'svhn' in dataset:
        mean = (0.5, 0.5, 0.5)
        std = (0.5, 0.5, 0.5)
        size, pad = 32, 0
    elif dataset == 'ImageNet1k':
        from .h5py_dataset import H5Dataset
        size,pad = 224,2
        mean = (0.485, 0.456, 0.406)
        std  = (0.229, 0.224, 0.225)
        #resize = 256
    
    if resize is None and bool((re.compile('imagenet', re.IGNORECASE)).search('ImageNet16-120')):
        resize = 16 
    elif resize is None and dataset in ['cifar', 'svhn']:
        resize = size 
    else:
        raise Exception('resize not specified')

    train_transform = transforms.Compose([
        transforms.RandomCrop(size, padding=pad),
        transforms.Resize(resize),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean,std),
    ])

    test_transform = transforms.Compose([
        transforms.Resize(resize),
        transforms.ToTensor(),
        transforms.Normalize(mean,std),
    ])

    if dataset == 'cifar10':
        train_dataset = CIFAR10(datadir, True, train_transform, download=True)
        test_dataset = CIFAR10(datadir, False, test_transform, download=True)
    elif dataset == 'cifar100':
        train_dataset = CIFAR100(datadir, True, train_transform, download=True)
        test_dataset = CIFAR100(datadir, False, test_transform, download=True)
    elif dataset == 'svhn':
        train_dataset = SVHN(datadir, split='train', transform=train_transform, download=True)
        test_dataset = SVHN(datadir, split='test', transform=test_transform, download=True)
    elif dataset == 'ImageNet16-120':
        train_dataset = ImageNet16(os.path.join(datadir, 'ImageNet16'), True , train_transform, 120)
        test_dataset  = ImageNet16(os.path.join(datadir, 'ImageNet16'), False, test_transform , 120)
    elif dataset == 'ImageNet1k':
        train_dataset = H5Dataset(os.path.join(datadir, 'imagenet-train-256.h5'), transform=train_transform)
        test_dataset  = H5Dataset(os.path.join(datadir, 'imagenet-val-256.h5'),   transform=test_transform)
            
    else:
        raise ValueError('There are no more cifars or imagenets.')

    train_dataset, valid_dataset = torch.utils.data.random_split(train_dataset, [len(train_dataset) - int(len(train_dataset) * valid_split), int(len(train_dataset) * valid_split)])

    train_loader = DataLoader(
        train_dataset,
        train_batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True)
    
    valid_loader = DataLoader(
        valid_dataset,
        valid_batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset,
        test_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True)

    if valid_split > 0:
        return train_loader, valid_loader, test_loader
    else:
        return train_loader, test_loader 
    # return train_loader, test_loader, valid_loader if valid_split > 0 else train_loader, test_loader


def get_mnist_dataloaders(train_batch_size, val_batch_size, num_workers):

    data_transform = Compose([transforms.ToTensor()])

    # Normalise? transforms.Normalize((0.1307,), (0.3081,))

    train_dataset = MNIST("_dataset", True, data_transform, download=True)
    test_dataset = MNIST("_dataset", False, data_transform, download=True)

    train_loader = DataLoader(
        train_dataset,
        train_batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True)
    test_loader = DataLoader(
        test_dataset,
        val_batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True)

    return train_loader, test_loader

import torch
import os
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
from torchvision.io import read_image
import pandas as pd
from torch.utils.data import DataLoader
from torchvision import transforms as torch_transforms
from torchvision.transforms import Compose, ToTensor, Normalize, Resize, PILToTensor
import numpy as np
import cv2
from skimage import io, transform
from PIL import Image
from torch.utils.data.dataloader import default_collate

class CustomImageDataset(torch.utils.data.Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        super(Dataset, self).__init__()
        self.img_labels = pd.read_csv(annotations_file, names=['file_name', 'label'])
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels) - 1

    def __getitem__(self, idx):
        img_path = self.img_labels.iloc[idx + 1, 0]
        # print(img_path)
        image = io.imread(img_path)
        image = Image.fromarray(image)
        label = int(self.img_labels.iloc[idx + 1, 1][0])
        if self.transform:
            image = self.transform(image)
        return image, label

def get_custom_data(annotations_file, img_dir, batch_size, transform=None, target_transform=None):
    mean = (0.4914, 0.4822, 0.4465)
    std = (0.2023, 0.1994, 0.2010)
    data_transform  = Compose([
                              Resize(32),
                              ToTensor(),
                              Normalize(mean, std),
                              ])
    data = CustomImageDataset(annotations_file, img_dir, data_transform, target_transform)
    train_loader = DataLoader(data,
                              batch_size,
                              shuffle=True,
                              num_workers=0,
                              pin_memory=True) 
    return train_loader