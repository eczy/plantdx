import argparse
import multiprocessing
import os
import shutil
import copy
import time
import numpy as np
import torch
import torchvision
from collections import defaultdict
from torchvision import models, transforms, datasets
from metrics import average_precision_multiclass

transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])
    ]),
    'eval':  transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485, 0.456, 0.406],
            [0.229, 0.224, 0.225])
    ])
}

def test(model, test_dl, metric, device='cpu'):
    model.eval()
    pred = []
    true = []
    for inputs, labels in test_dl:
        inputs = inputs.to(device)
        labels = labels.to(device)
        
        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            
        pred.extend(outputs.cpu().data.numpy())
        true.extend(labels.cpu().data.numpy())

    score = metric(np.array(true), np.array(pred))
    print(f'Test score: {score}')

def main():
    np.random.seed(0)
    torch.manual_seed(0)
    parser = argparse.ArgumentParser()
    parser.add_argument('test_dir', metavar='test-dir')
    parser.add_argument('model_path', metavar='model-path')
    parser.add_argument('--batch-size', default=4, type=int)
    parser.add_argument('--nthreads', default=-1)
    parser.add_argument('--cuda', action='store_true')
    args = parser.parse_args()
    
    if args.nthreads < 0:
        args.nthreads = multiprocessing.cpu_count()
    print(f'Using {args.nthreads} threads.')
        
    device = torch.device('cuda:0' if args.cuda and torch.cuda.is_available() else 'cpu')
    print(f'{"U" if args.cuda else "Not u"}sing GPU acceleration.')
    
    test_ds = datasets.ImageFolder(args.test_dir, transforms['eval'])
    
    print(f'Test samples: {len(test_ds)}')

    test_dl = torch.utils.data.DataLoader(test_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.nthreads)
    
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Linear(model.fc.in_features, len(test_ds.classes))
    model.load_state_dict(torch.load(args.model_path))
    model.to(device)
    
    test(model, test_dl, average_precision_multiclass, device=device)

if __name__ == '__main__':
    main()