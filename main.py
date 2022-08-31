

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
        '-cli','--clini',help = 'Path to clini table (excel format), eg: /media/JD/LIVER/TCGA-LIVER-HCC/tables/CLINI.xlsx'
    )
    parser.add_argument(
        '-sli','--slide',help = 'Path to slide table (csv format), eg: /media/JD/LIVER/TCGA-LIVER-HCC/tables/SLIDE.csv'
    )
    parser.add_argument(
        '-F','--desired_feats',nargs='*',choices = ['resnet18','xiyue','HIPT'],required = True,help='List of pre-extracted features to try, choices: resnet18, xiyue, HIPT'
    )
    parser.add_argument(
        '-A','--use_annotated',action='store_true',help = 'Flag if you want to look at annotated_features folders'
    )
    parser.add_argument(
        '-O','--output_path',required = True,help='Path to save all outputs'
    )
    parser.add_argument(
        '-n','--n_folds',nargs='*',type=int,help='Number of folds for cross-validation, can input int or list',default=3
    )
    parser.add_argument(
        '-lr','--learning_rates',nargs='*',type=float,help='Learning rate(s) to try, can be list or single number',default=1e-4
    )
    parser.add_argument(
        '-bs','--batch_size',nargs='*',type=int,help='Batch sizes to try, can be list or int',default =64
    )
    parser.add_argument(
        '-T','--target_label',nargs='*',required=True,help='Target label(s) to train for, will accept list'
    )
    parser.add_argument(
        '-r','--runs',type=int,help='Number of runs to do for each combination of hyperparameters',default=1
    )

    return parser.parse_args()

########## Main ##########

args = get_args()

Cohort = args.cohort
desired_feats = args.desired_feats if isinstance(args.desired_feats,list) else [args.desired_feats]
feature_dirs = src.loading_utils.find_feat_folders(Cohort,desired_feats,args.use_annotated)
if not(args.clini and args.slide):
    clini_excel,slide_csv = src.loading_utils.find_tables(Cohort)
else:
    clini_excel = args.clini
    slide_csv = args.slide
n_folds = args.n_folds if isinstance(args.n_folds,list) else [args.n_folds]
learning_rates = args.learning_rates if isinstance(args.learning_rates,list) else [args.learning_rates]
batch_sizes = args.batch_size if isinstance(args.batch_size,list) else [args.batch_size]
out_path_root = args.output_path
runs = args.runs

output = [['Target_Label','Model','Features','Run','Fold','Learning_rate','Batch_size','epoch','train_loss','valid_loss','roc_auc_score']]

for t in tqdm(args.target_label): # loop over target labels
    for i in tqdm(range(len(desired_feats))): # loop over feature selection
        f = feature_dirs[i]
        for n in tqdm(n_folds): # loop over number of folds selected
            for lr in tqdm(learning_rates): # loop over learning rates
                for bsize in tqdm(batch_sizes): # loop over batch sizes
                    params={ # set parameters for this particular combination
                            'clini':clini_excel,
                            'slide':slide_csv,
                            'output':out_path_root,
                            'feats':f,
                            'target':t,
                            'lr':lr,
                            'bsize':bsize,
                            'n_splits':n,
                            'runs':runs
                            }
                    output_paths = src.training_utils.train_one_combo(params) # run the training step
                    for j in range(runs): # for each run
                        for k in range(n): # for each fold within a run
                            # get the best performing model's stats
                            new_data = src.training_utils.get_best_stats(os.path.join(output_paths[j],'fold-{}'.format(k),'history.csv'))
                            idx = new_data.iloc[0,0]
                            new_row = ['{}'.format(t),'MIL',desired_feats[i],'{}/{}'.format(j,runs-1),'{}/{}'.format(k,n-1),params['lr'],params['bsize'],new_data.loc[idx,'epoch'],new_data.loc[idx,'train_loss'],new_data.loc[idx,'valid_loss'],new_data.loc[idx,'roc_auc_score']]
                            output.append(new_row) # add the new stats


with open(os.path.join(out_path_root,'stats.csv'),'w') as f:
    # save output to stats.csv
    writer = csv.writer(f)
    writer.writerows(output)

print('Done! You can find your results at {}'.format(os.path.join(out_path_root,'stats.csv')))