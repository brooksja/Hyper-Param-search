

########## Packages ##########

import os
from re import T
import numpy as np
from tqdm import tqdm
import h5py
import pytorch_lightning as pl
import pandas as pd
import csv
import argparse

import src.loading_utils
import src.training_utils
import marugoto.mil as mil

########## Set up parser ##########
def get_args():
    parser = argparse.ArgumentParser(description = 'Script to loop through desired hyper parameters and return the best models')

    parser.add_argument(
        '-C','--cohort',required = True,help = 'Path to cohort of interest, eg: /media/JD/LIVER/TCGA-LIVER-HCC/'
    )
    parser.add_argument(
        '-F','--desired_feats',nargs='*',choices = ['resnet18','xiyue','HIPT'],required = True,help='List of pre-extracted features to try, choices: resnet18, xiyue, HIPT'
    )
    parser.add_argument(
        '-O','--output_path',required = True,help='Path to save all outputs'
    )
    parser.add_argument(
        '-n','--n_folds',nargs='*',type=int,help='Number of folds for cross-validation, can input int or list',default=3
    )
    parser.add_argument(
        '-lr','--learning_rates',nargs='*',type=float,help='learning rate(s) to try, can be list or single number',default=1e-4
    )
    parser.add_argument(
        '-bs','--batch_size',nargs='*',type=int,help='Batch sizes to try, can be list or int',default =64
    )
    parser.add_argument(
        '-T','--target_label',required=True,help='Target label to train for'
    )

    return parser.parse_args()

########## Main ##########

args = get_args()

Cohort = args.cohort
desired_feats = args.desired_feats if isinstance(args.desired_feats,list) else [args.desired_feats]
feature_dirs = src.loading_utils.find_feat_folders(Cohort,desired_feats)
clini_excel,slide_csv = src.loading_utils.find_tables(Cohort)
n_folds = args.n_folds if isinstance(args.n_folds,list) else [args.n_folds]
learning_rates = args.learning_rates if isinstance(args.learning_rates,list) else [args.learning_rates]
batch_sizes = args.batch_size if isinstance(args.batch_size,list) else [args.batch_size]
out_path_root = args.output_path

output = [['Model','Features','Fold','Learning_rate','Batch_size','epoch','train_loss','valid_loss','roc_auc_score']]

for i in tqdm(range(len(desired_feats))):
    f = feature_dirs[i]
    for n in tqdm(n_folds):
        for lr in tqdm(learning_rates):
            for bsize in tqdm(batch_sizes):
                params={
                        'clini':clini_excel,
                        'slide':slide_csv,
                        'output':out_path_root,
                        'feats':f,
                        'target':args.target_label,
                        'lr':lr,
                        'bsize':bsize,
                        'n_splits':n
                        }
                output_path = src.training_utils.train_one_combo(params)
                for j in range(n):
                    new_data = src.training_utils.get_best_stats(os.path.join(output_path,'fold-{}'.format(j),'history.csv'))
                    idx = new_data.iloc[0,0]
                    new_row = ['MIL',desired_feats[i],'{}/{}'.format(j,n-1),params['lr'],params['bsize'],new_data.loc[idx,'epoch'],new_data.loc[idx,'train_loss'],new_data.loc[idx,'valid_loss'],new_data.loc[idx,'roc_auc_score']]
                    output.append(new_row)


with open(os.path.join(out_path_root,'stats.csv'),'w') as f:
    writer = csv.writer(f)
    writer.writerows(output)

print('Done! You can find your results at {}'.format(os.path.join(out_path_root,'stats.csv')))