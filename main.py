########## Packages ##########

import os
from re import T
import numpy as np
from tqdm import tqdm
import h5py
import pytorch_lightning as pl
import pandas as pd
import csv

from src.loading_utils import check_hyperparams
import src.training_utils
import marugoto.mil as mil
from src.GUI import HPGUI
import src.error_handling as eh


########## Main ##########

# Get hyperparameter input through GUI
HP = HPGUI()

# check each hyperparameter is in the desired format/is present/etc
HP.hyperparams = check_hyperparams(HP.hyperparams)

output = [['Target_Label','Model','Features','Run','Fold','Learning_rate','Batch_size','bag_size','epoch','train_loss','valid_loss','roc_auc_score']]

for t in tqdm(HP.hyperparams['targets']): # loop over target labels
    for f in tqdm(HP.hyperparams['feats']): # loop over feature selection
        for n in tqdm(HP.hyperparams['folds']): # loop over number of folds selected
            for lr in tqdm(HP.hyperparams['learning_rates']): # loop over learning rates
                for bsize in tqdm(HP.hyperparams['batch_sizes']): # loop over batch sizes
                    for bag_size in tqdm(HP.hyperparams['bag_sizes']): # loop over bag sizes
                        params={ # set parameters for this particular combination
                            'clini':HP.hyperparams['clini_path'],
                            'slide':HP.hyperparams['slide_path'],
                            'output':HP.hyperparams['output_path'],
                            'feats':f,
                            'target':t,
                            'lr':lr,
                            'bsize':bsize,
                            'n_splits':n,
                            'runs':HP.hyperparams['runs'],
                            'bag_size':bag_size 
                        }
                        output_paths = src.training_utils.train_one_combo(params) # run the training step
                        for j in range(HP.hyperparams['runs']): # for each run
                            for k in range(n): # for each fold within a run
                                # get the best performing model's stats
                                new_data = src.training_utils.get_best_stats(os.path.join(output_paths[j],'fold-{}'.format(k),'history.csv'))
                                idx = new_data.iloc[0,0]
                                new_row = ['{}'.format(t),'MIL',f,'{}/{}'.format(j,HP.hyperparams['runs']-1),'{}/{}'.format(k,n-1),params['lr'],params['bsize'],params['bag_size'],new_data.loc[idx,'epoch'],new_data.loc[idx,'train_loss'],new_data.loc[idx,'valid_loss'],new_data.loc[idx,'roc_auc_score']]
                                output.append(new_row) # add the new stats


with open(os.path.join(HP.hyperparams['output_path'],'stats.csv'),'w') as f:
    # save output to stats.csv
    writer = csv.writer(f)
    writer.writerows(output)

print('Done! You can find your results at {}'.format(os.path.join(HP.hyperparams['output_path'],'stats.csv')))


