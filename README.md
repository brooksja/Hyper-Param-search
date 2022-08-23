# Harry-Potter-Hyper-Params
Project to centralise and streamline hyper parameter tuning and model selection


## Instructions
1. Clone repo
3. Create env from requirments.txt TODO
5. Run python /path/to/main.py -C /path/to/cohort -F {'resnet18',xiyue','HIPT'} -O /path/to/output -T 'target_label'

## Options in full
-C --cohort           /path/to/cohort             REQUIRED

-F --desired_feats    {'resnet18',xiyue','HIPT'}  REQUIRED choice, accepts list

-O --output_path      /path/to/output             REQUIRED

-T --target_label     'target_label'              REQUIRED

-n --n_folds          int                         OPTIONAL accepts list

-lr --learning_rates  float                       OPTIONAL accepts list

-bs --batch_size      int                         OPTIONAL accepts list
