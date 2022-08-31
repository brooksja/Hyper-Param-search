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
    n_splits = params['splits'] if 'splits' in params.keys() else 3
    lr = params['lr'] if 'lr' in params.keys() else 1e-4
    bsize = params['bsize'] if 'bsize' in params.keys() else 64
    runs = params['runs'] if 'runs' in params.keys() else 1

    output_paths = []

    for r in range(runs):
        # make a path for the output based on original specification + this iteration's hyper params
        output_path = os.path.join(output_path_root,target_label+'_'+os.path.basename(feature_dir)+'_bs={}_lr={}_nfolds={}'.format(bsize,lr,n_splits),'Run_{}'.format(r))
        output_paths.append(output_path)

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
                        batch_size=bsize)
    return output_paths
    
def get_best_stats(outpath):
    df = pd.read_csv(outpath)
    best_model_row = df.loc[df['valid_loss']==min(df['valid_loss'])]
    return best_model_row