# Module containing functions to pass parameters and train models

########## Packages ##########
import marugoto.mil as mil
from tqdm import tqdm
from typing import Iterable,Sequence,Optional
import os

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
            