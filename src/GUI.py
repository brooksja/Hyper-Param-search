########## Packages ##########

import tkinter as tk

########## Define GUI ##########
# Idea: streamline hyperparameter tuning by using a GUI instead of command line
class HPGUI():
    def __init__(self):
        self.hyperparams = {}
        self.window = tk.Tk(className=' Hyper-Param-search') # Create window
        self.window.rowconfigure([0,1],weight=1,minsize=50)
        self.window.columnconfigure([0,1,2],weight=1,minsize=20)

        # frame to get clini table location
        frm_clini = tk.Frame(master = self.window,borderwidth=1)
        frm_clini.grid(row=0,column=0,padx=2,pady=2)
        lbl_clini = tk.Label(master=frm_clini,text='Specify path to clini table (should be .xlsx)')
        lbl_clini.pack()
        self.ent_clini = tk.Entry(master=frm_clini,width=80)
        self.ent_clini.pack()
        lbl_output = tk.Label(master=frm_clini,text='Specify path for output')
        lbl_output.pack()
        self.ent_output = tk.Entry(master=frm_clini,width=80)
        self.ent_output.pack()

        # frame to get table location
        frm_slide = tk.Frame(master = self.window,borderwidth=1)
        frm_slide.grid(row=0,column=1,padx=2,pady=2)
        lbl_slide = tk.Label(master=frm_slide,text='Specify path to slide table (should be .csv)')
        lbl_slide.pack()
        self.ent_slide = tk.Entry(master=frm_slide,width=80)
        self.ent_slide.pack()
        lbl_runs = tk.Label(master=frm_slide,text='Specify number of runs for each combination to do')
        lbl_runs.pack()
        self.ent_runs = tk.Entry(master=frm_slide,width=80)
        self.ent_runs.pack()

        # 1st frame asks for target labels
        frm_targets = tk.Frame(master = self.window,borderwidth=1)
        frm_targets.grid(row=1,column=0,padx=2,pady=2)
        lbl_targets = tk.Label(master=frm_targets,text='Specify target labels (one per line)')
        lbl_targets.pack()
        self.txt_targets = tk.Text(master=frm_targets)
        self.txt_targets.pack()

        # 2nd frame asks for features to use
        frm_feats = tk.Frame(master = self.window,borderwidth=1)
        frm_feats.grid(row=1,column=1,padx=2,pady=2)
        lbl_feats = tk.Label(master=frm_feats,text='Specify feature directories to use (one per line)')
        lbl_feats.pack()
        self.txt_feats = tk.Text(master=frm_feats)
        self.txt_feats.pack()

        # 3rd frame asks for number of folds to do
        frm_folds = tk.Frame(master = self.window,borderwidth=1)
        frm_folds.grid(row=1,column=2,padx=2,pady=2)
        lbl_folds = tk.Label(master=frm_folds,text='Specify numbers of folds to try (one per line)')
        lbl_folds.pack()
        self.txt_folds = tk.Text(master=frm_folds)
        self.txt_folds.pack()

        # 4th frame asks for learning rates
        frm_lr = tk.Frame(master = self.window,borderwidth=1)
        frm_lr.grid(row=2,column=0,padx=2,pady=2)
        lbl_lr = tk.Label(master=frm_lr,text='Specify learning rates to try (one per line)')
        lbl_lr.pack()
        self.txt_lr = tk.Text(master=frm_lr)
        self.txt_lr.pack()

        # 5th frame asks for batch sizes
        frm_bs = tk.Frame(master = self.window,borderwidth=1)
        frm_bs.grid(row=2,column=1,padx=2,pady=2)
        lbl_bs = tk.Label(master=frm_bs,text='Specify batch sizes to try (one per line)')
        lbl_bs.pack()
        self.txt_bs = tk.Text(master=frm_bs)
        self.txt_bs.pack()

        # 6th frame asks for bag sizes
        frm_bags = tk.Frame(master = self.window,borderwidth=1)
        frm_bags.grid(row=2,column=2,padx=2,pady=2)
        lbl_bags = tk.Label(master=frm_bags,text='Specify bag sizes to try (one per line)')
        lbl_bags.pack()
        self.txt_bags = tk.Text(master=frm_bags)
        self.txt_bags.pack()

        # Frame for start button
        frm_start = tk.Frame(master = self.window,borderwidth=1)
        frm_start.grid(row=0,column=2,padx=2,pady=2)
        lbl_start = tk.Label(master=frm_start,text='Hit button to start hyperparameter tuning!')
        lbl_start.pack()
        btn_start = tk.Button(master=frm_start,text='START',bg='red',width=25,height=10,command=lambda:self.handle_click())
        btn_start.pack()
        #btn_start.bind('<Button-1>',self.handle_click)

        self.window.mainloop()

    # Code to handle the button being clicked
    def handle_click(self,event=None):
        self.hyperparams['clini_path'] = self.ent_clini.get()
        self.hyperparams['slide_path'] = self.ent_slide.get()
        self.hyperparams['output_path'] = self.ent_output.get()
        self.hyperparams['runs'] = self.ent_runs.get()
        self.hyperparams['targets'] = self.txt_targets.get('1.0',tk.END)
        self.hyperparams['feats'] = self.txt_feats.get('1.0',tk.END)
        self.hyperparams['folds'] = self.txt_folds.get('1.0',tk.END)
        self.hyperparams['learning_rates'] = self.txt_lr.get('1.0',tk.END)
        self.hyperparams['batch_sizes'] = self.txt_bs.get('1.0',tk.END)
        self.hyperparams['bag_sizes'] = self.txt_bags.get('1.0',tk.END)

        self.window.destroy()
        # use HPGUI.hyperparameters to access dictionary

