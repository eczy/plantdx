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

def train(model, train_dl, val_dl, criterion, optimizer, metric, output_dir, device='cpu', patience=None, checkpoint_rate=None):
    start = time.time()
    best_weights = copy.deepcopy(model.state_dict())
    best_score = 0.0
    
    losses = defaultdict(list)
    scores = defaultdict(list)
    last_improvement = 0
    epoch = 0
    while epoch - last_improvement < patience:
        for phase, dl in zip(['train', 'val'], [train_dl, val_dl]):
            if phase == 'train':
                model.train()
            else:
                model.eval()
                
            total_loss = 0.0
            y_pred = []
            y_true = []
            for inputs, labels in dl:
                inputs = inputs.to(device)
                labels = labels.to(device)
                
                optimizer.zero_grad()
                
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
                    
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()
                
                total_loss += loss.item() * inputs.size(0)
                y_pred.extend(outputs.cpu().data.numpy())
                y_true.extend(labels.cpu().data.numpy())
            
            score = metric(np.array(y_true), np.array(y_pred))
            scores[phase].append(score)
            losses[phase].append(total_loss)
            np.save(os.path.join(output_dir, f'{phase}_loss.npy'), np.array(losses[phase]))
            np.save(os.path.join(output_dir, f'{phase}_score.npy'), np.array(scores[phase]))
            
            if epoch % checkpoint_rate == 0:
                elapsed = time.time() - start
                minutes = elapsed // 60 % 60
                seconds = elapsed % 60
                print(f'[{phase}]\t epoch: {epoch} loss: {loss:.4f} score: {score:.4f} elapsed: {minutes}m {seconds:.2f}s patience: {patience - (epoch - last_improvement)}')
                
            if phase == 'val' and score > best_score:
                best_score = score
                torch.save(model.state_dict(), os.path.join(output_dir, 'model.pt'))
                torch.save(optimizer.state_dict(), os.path.join(output_dir, 'optimizer.pt'))
                last_improvement = epoch
        epoch += 1
    

def main():
    np.random.seed(0)
    torch.manual_seed(0)
    parser = argparse.ArgumentParser()
    parser.add_argument('train_dir', metavar='train-dir')
    parser.add_argument('val_dir', metavar='val-dir')
    parser.add_argument('output_dir', metavar='output-dir')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--lr', default=0.001)
    parser.add_argument('--patience', default=-1, type=int)
    parser.add_argument('--checkpoint-rate', default=100, type=int)
    parser.add_argument('--batch-size', default=4, type=int)
    parser.add_argument('--nthreads', default=-1)
    parser.add_argument('--cuda', action='store_true')
    args = parser.parse_args()
    
    if args.nthreads < 0:
        args.nthreads = multiprocessing.cpu_count()
    print(f'Using {args.nthreads} threads.')
        
    device = torch.device('cuda:0' if args.cuda and torch.cuda.is_available() else 'cpu')
    print(f'{"U" if args.cuda else "Not u"}sing GPU acceleration.')
    
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    elif args.force:
        shutil.rmtree(args.output_dir)
        os.mkdir(args.output_dir)
    else:
        raise FileExistsError('Output directory already exists.')
    
    train_ds = datasets.ImageFolder(args.train_dir, transforms['train'])
    val_ds = datasets.ImageFolder(args.val_dir, transforms['eval'])
    
    print(f'Train samples: {len(train_ds)}')
    print(f'Val samples: {len(val_ds)}')

    train_dl = torch.utils.data.DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=args.nthreads)
    val_dl = torch.utils.data.DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.nthreads)
    
    model = models.resnet18(pretrained=True)
    model.fc = torch.nn.Linear(model.fc.in_features, len(train_ds.classes))
    model.to(device)

    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    
    train(model, train_dl, val_dl, criterion, optimizer, average_precision_multiclass, args.output_dir, device=device, patience=args.patience, checkpoint_rate=args.checkpoint_rate)
        
if __name__ == '__main__':
    main()