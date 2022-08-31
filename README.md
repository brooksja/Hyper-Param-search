# Hyper-Param-search
Project to centralise and streamline hyper parameter tuning and model selection


## Instructions
1. Clone repo
3. Create env from requirments.txt
5. Run python /path/to/main.py -C /path/to/cohort -F {'resnet18',xiyue','HIPT'} -O /path/to/output -T 'target_label'

## Options in full
-C --cohort           /path/to/cohort             REQUIRED

-cli --clini          /path/to/table/clini.xlsx   OPTIONAL if not specified, will try to find automatically, if used enter -sli too!

-sli --slide          /path/to/table/slide.csv    OPTIONAL if not specified, will try to find automatically, if used enter -cli too!

-F --desired_feats    {'resnet18',xiyue','HIPT'}  REQUIRED choice, accepts list

-A --use_annotated                                OPTIONAL flag if you want to look at features_annotated folders (only)

-O --output_path      /path/to/output             REQUIRED

-T --target_label     'target_label'              REQUIRED

-n --n_folds          int                         OPTIONAL accepts list

-lr --learning_rates  float                       OPTIONAL accepts list

-bs --batch_size      int                         OPTIONAL accepts list

-r --runs             int                         OTPIONAL

## File structure
For automatic searching, the following file structure is assumed:

.../cohort/

--> features/

    --> xiyue

    --> resnet18

    --> HIPT

--> tables/

    --> clini.xlsx

    --> slide.csv

--> features_annotated/

    --> xiyue

    --> resnet18

    --> HIPT

## Marugoto
Marugoto from https://github.com/KatherLab/marugoto.git, please also cite their work if using!
