# module containing functions to handle data loading

########## Packages ##########

import os
import src.error_handling as eh


########## Functions ##########

def check_hyperparams(hyperparams):
    # function to check hyperparameters and convert to desired format

    # first, check table paths were entered
    if not(hyperparams['clini_path']):
        raise eh.NoDataError(message='Path to clini table missing')
    if not(hyperparams['slide_path']):
        raise eh.NoDataError(message='Path to slide table missing')
    if not(hyperparams['output_path']):
        raise eh.NoDataError(message='Output path missing')
    
    # check paths exist
    if not(os.path.exists(hyperparams['clini_path'])):
        raise eh.BadPathError('Cannot find clini table at '+hyperparams['clini_path'])
    if not(os.path.exists(hyperparams['slide_path'])):
        raise eh.BadPathError('Cannot find slide table at '+hyperparams['slide_path'])
    # if output path does not exist, create it
    if not(os.path.exists(hyperparams['slide_path'])):
        raise os.makedirs(hyperparams['output_path'])

    # split remaining hyperparameters into lists
    for key in list(hyperparams.keys())[4:]:
        hyperparams[key] = hyperparams[key].split('\n')[:-1]
        # convert folds, batch_sizes, bag_sizes to int and learning_rates to float
        if key in ('folds','batch_sizes','bag_sizes'):
            for i in range(len(hyperparams[key])):
                if hyperparams[key][i] == '':
                    hyperparams[key][i] = []
                else:
                    hyperparams[key][i] = int(hyperparams[key][i])
        if key in ('learning_rates'):
            for i in range(len(hyperparams[key])):
                if hyperparams[key][i] == '':
                    hyperparams[key][i] = []
                else:
                    hyperparams[key][i] = float(hyperparams[key][i])
    
    # if runs is empty or zero, set it to a default of 1 (all other params have defaults set elsewhere)
    if not(hyperparams['runs']) or hyperparams['runs']==0:
        hyperparams['runs'] = 1
    else:
        hyperparams['runs'] = int(hyperparams['runs'])

    return hyperparams