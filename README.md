# Hyper-Param-search
Project to centralise and streamline hyper parameter tuning and model selection


## Instructions
1. Clone repo
3. Create env from requirments.txt
5. Run python /path/to/main.py -C /path/to/cohort -F {'resnet18',xiyue','HIPT'} -O /path/to/output -T 'target_label'

## Options in full
-C --cohort           /path/to/cohort             REQUIRED

-F --desired_feats    {'resnet18',xiyue','HIPT'}  REQUIRED choice, accepts list

-A --use_annotated                                OPTIONAL flag if you want to look at features_annotated folders (only)

-O --output_path      /path/to/output             REQUIRED

-T --target_label     'target_label'              REQUIRED accepts list

-n --n_folds          int                         OPTIONAL accepts list

-lr --learning_rates  float                       OPTIONAL accepts list

-bs --batch_size      int                         OPTIONAL accepts list

-r --runs             int                         OTPIONAL


Marugoto from https://github.com/KatherLab/marugoto.git, please also cite their work if using!
