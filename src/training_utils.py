# Module containing functions to pass parameters and train models

########## Packages ##########
import marugoto.mil as mil
from tqdm import tqdm
from typing import Iterable,Sequence,Optional
import os
import pandas as pd

########## Functions ##########
def train_one_combo(params):
    # extract variables from dict
    # essential variables
    clini_excel = params['clini']
    slide_csv = params['slide']
    output_path_root = params['output']
    feature_dir = params['feats']
    target_label = params['target']

    # optional variables
    n_splits = params['n_splits'] if 'n_splits' in params.keys() else 3
    lr = params['lr'] if 'lr' in params.keys() else 1e-4
    bsize = params['bsize'] if 'bsize' in params.keys() else 64
    runs = params['runs'] if 'runs' in params.keys() else 1
    bag_size = params['bag_size'] if 'bag_size' in params.keys() else 512

    output_paths = []

    for r in range(runs):
        # make a path for the output based on original specification + this iteration's hyper params
        if feature_dir.find('/',-1) == len(feature_dir)-1:
            # if the feature_dir ends in a '/', remove the last character
            feature_dir = feature_dir[:-1]
        feature_string = os.path.basename(os.path.dirname(feature_dir))+'-'+os.path.basename(feature_dir)
        output_path = os.path.join(output_path_root,target_label+'_'+feature_string+'_bs={}_lr={}_nfolds={}_bagsize={}'.format(bsize,lr,n_splits,bag_size),'Run_{}'.format(r))
        output_paths.append(output_path)

        # run marugoto cross-val for the current set of hyperparameters
        mil.helpers.categorical_crossval_(
                        clini_excel=clini_excel,
                        slide_csv=slide_csv,
                        feature_dir=feature_dir,
                        output_path=output_path,
                        target_label=target_label,
                        cat_labels=[],
                        cont_labels=[],
                        n_splits=n_splits,
                        categories=None,
                        lr_max=lr,
                        batch_size=bsize,
                        bag_size=bag_size)
    return output_paths
    
def get_best_stats(outpath):
    # find the best model by finding the one with the minimum validation loss
    df = pd.read_csv(outpath)
    best_model_row = df.loc[df['valid_loss']==min(df['valid_loss'])]
    return best_model_row
