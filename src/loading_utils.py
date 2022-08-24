# module containing functions to handle data loading

########## Packages ##########

import os


########## Functions ##########

def find_feat_folders(Cohort_Path,Desired_Feats):
    # Function walks through cohort folder looking for feature folders
    # Returns: list of paths to feature folders
    Feat_Paths = []
    Base_Paths = []
    for root,dirs,_ in os.walk(Cohort_Path):
        [Base_Paths.append(os.path.join(root,d)) for d in dirs if 'feature' in d if not('annotated' in d)] # checks for folders containing features but ignores annotated
    
    for f in Desired_Feats:
    # generate path to folder of features
        if f == 'HIPT':
            p = [g for g in Base_Paths if 'HIPT' in g][0]
            if 'HIPT_features' in p:
                Feat_Paths.append(p)
            else:
                Feat_Paths.append(os.path.join(p,f))
        else:
            p = [g for g in Base_Paths if not('HIPT' in g)][0]
            Feat_Paths.append(os.path.join(p,f))
    
    return Feat_Paths

def find_tables(Cohort_Path):
    for root,_,files in os.walk(Cohort_Path):
        for f in files:
            if ('CLINI' in f) and (os.path.splitext(f)[1]=='.xlsx'):
                clini_excel = os.path.join(root,f)
            if ('SLIDE' in f) and (os.path.splitext(f)[1]=='.csv'):
                slide_csv = os.path.join(root,f)
    if clini_excel and slide_csv:
        return clini_excel,slide_csv
    else:
        print('Problem finding tables...')