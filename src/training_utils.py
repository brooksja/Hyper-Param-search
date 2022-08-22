# Module containing functions to pass parameters and train models

########## Packages ##########
import marugoto.mil as mil
from tqdm import tqdm
from typing import Iterable,Sequence,Optional
import os
import pandas as pd

########## Functions ##########
def hyper_param_sweep(
    clini_excel: str,
    slide_csv: str,
    output_path_root: str,
    feature_dirs: Iterable[str],
    target_label: str,
    cat_labels: Sequence[str] = [],
    cont_labels: Sequence[str] = [],
    n_splits: int = 5,
    categories: Optional[Iterable[str]] = None,
    learning_rates: Iterable[float] = [1e-4],
    batch_sizes: Iterable[int] = [64],
):
    for feature_dir in tqdm(feature_dirs):
        for Bsize in tqdm(batch_sizes):
            for lr in tqdm(learning_rates):
                # make a path for the output based on original specification + this iteration's hyper params
                output_path = os.path.join(output_path_root,os.path.basename(feature_dir)+'_batch_size={}_lr={}'.format(Bsize,lr))
                # run crossval
                mil.helpers.categorical_crossval_(
                    clini_excel=clini_excel,
                    slide_csv=slide_csv,
                    feature_dir=feature_dir,
                    output_path=output_path,
                    target_label=target_label,
                    cat_labels=cat_labels,
                    cont_labels=cont_labels,
                    n_splits=n_splits,
                    categories=categories,
                    lr_max=lr,
                    batch_size=Bsize)
            

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

    # make a path for the output based on original specification + this iteration's hyper params
    output_path = os.path.join(output_path_root,os.path.basename(feature_dir)+'_batch_size={}_lr={}'.format(bsize,lr))

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
    return output_path
    
def get_best_stats(outpath):
    df = pd.read_csv(outpath)
    best_model_row = df.loc[df['valid_loss']==min(df['valid_loss'])]
    return best_model_row