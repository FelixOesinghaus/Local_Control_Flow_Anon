from check_model_quality import check_model_quality as check_model_quality
from generate_process_model import generate_process_model as generate_process_model
import sys
from pm4py.objects.log.importer.xes import importer as xes_importer
import os
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

#log_name = 'Road_Traffic_Fine_Management_Process'
#folder_name = "traffic"
#log_name = 'Sepsis_Cases_-_Event_Log'
#folder_name = "sepsis"

file_name = ["Sepsis_Cases_-_Event_Log.xes","WABO_CoSeLoG_project.xes","Road_Traffic_Fine_Management_Process.xes"]

folder_name = ["sepsis","coselog","traffic"]


epsRange = [0.01, 0.1, 1.0]


# choose from f_score, generalization, log_fitness, simplicity , precision
value_to_be_plotted = "precision"

title_value = ""
if value_to_be_plotted == "generalization":
    title_value = "Generalization"
if value_to_be_plotted == "f_score":
    title_value = "F-Score"
if value_to_be_plotted == "log_fitness":
    title_value = "Log Fitness"
if value_to_be_plotted == "simplicity":
    title_value = "Simplicity"
if value_to_be_plotted == "precision":
    title_value = "Precision"

#base_path = os.getcwd() + os.sep + folder_name + os.sep

#os.environ["PATH"] += os.pathsep + 'C:' + os.pathsep + 'users' + os.pathsep + 'oesinghaus' + os.pathsep + 'appdata' + os.pathsep + 'local' + os.pathsep + 'programs' + os.pathsep + 'python'+ os.pathsep + 'python36'+ os.pathsep + 'lib'+ os.pathsep + 'site-packages'+ os.pathsep + 'C:'

tries = 10
all_labels = ["DFG Approach","TVQ baseline"]

for k in range(len(file_name)):
    fig, axs = plt.subplots(1,len(epsRange))
    
    if folder_name[k]=='sepsis':
        fig.suptitle('Sepsis')
    if folder_name[k]=='coselog':
        fig.suptitle('CoSeLog')
    if folder_name[k]=='traffic':
        fig.suptitle('Traffic Fines')
        
    DF_list = list()
    DF_list_pripel = list()
    
    boxplots = list()
    #DF_list.append(pd.DataFrame(columns = column_names))
    #print(k)
    base_path = os.getcwd() + os.sep + folder_name[k] + os.sep
    base_path_pripel = os.getcwd() + os.sep +"pripel"+ os.sep + folder_name[k] + os.sep
    
    load_path = base_path + folder_name[k] + "_fitness.csv"
    load_path_pripel = base_path_pripel + folder_name[k] + "_fitness.csv"
    
    full_df = pd.read_csv(load_path, sep=',')
    full_df_pripel = pd.read_csv(load_path_pripel, sep=',')
    
    trace_names = full_df.columns.values.tolist()
    list_of_traces = trace_names[1:len(trace_names)-1]
    
    #df_original = full_df[full_df['epsilon'] == 99.9]
    #df_original = df_original.drop(["Unnamed: 0","epsilon"],axis=1)
    #orig_values_list_of_lists = df_original.values.tolist()
    #orig_values = orig_values_list_of_lists[0]
    
    one_to_twenty = list(range(1, 21))

    for m in range(len(epsRange)):
    
        DF_list.append(full_df[full_df['epsilon'] == epsRange[m]].drop(["Unnamed: 0","epsilon"],axis=1))
        DF_list_pripel.append(full_df_pripel[full_df_pripel['epsilon'] == epsRange[m]].drop(["Unnamed: 0","epsilon"],axis=1))
        plt.sca(axs[m])
        plt.grid(axis='y')
        plt.xticks(range(1,3),rotation = 15)
        
        f_scores = DF_list[m][value_to_be_plotted].tolist()################################
        f_scores_pripel = DF_list_pripel[m][value_to_be_plotted].tolist()#############################
        
        f_scores_np_array = np.asarray(f_scores)
        f_scores_pripel_np_array = np.asarray(f_scores_pripel)
        f_scores_data = [ f_scores_np_array, f_scores_pripel_np_array]
        print(f_scores_data)
        print(type(f_scores_data))
        #means = DF_list[m].mean(axis=0).tolist()
        #pripel_means = DF_list_pripel[m].mean(axis=0).tolist()
        #max = DF_list[m].max(axis=0).tolist()
        #min = DF_list[m].min(axis=0).tolist()
        #print(f_scores)
        #sys.exit()
        boxplot_current = axs[m].boxplot(f_scores_data,vert=True,patch_artist=True,labels=all_labels)
        boxplots.append(boxplot_current)
        #axs[m].plot(one_to_twenty,pripel_means,color='black', linestyle='dashed',label="PRIPEL baseline avg.")
        #axs[m].plot(one_to_twenty,pripel_means,color='black', linestyle='dashed',label="PRIPEL baseline avg.")
        
        #axs[m].plot(one_to_twenty,max,color='green', linestyle='dotted',label="Maximum occurrence")
        #axs[m].plot(one_to_twenty,min,color='blue', linestyle='dotted',label="Minimum occurrence")
        #axs[m].plot(one_to_twenty,means,color='red',label="Average occurrence")
        #axs[m].scatter(one_to_twenty,orig_values,label="Original trace frequencies")
        
        
        #axs[m].set_xlabel("20 most frequent trace variants")
        #axs[m].set_ylabel("F-Score")
        axs[0].set_ylabel(title_value)
        axs[m].set_ylim([0.0,1.0])
        #axs[m].set_title(r'$\epsilon$ = ' + r'%s' % (epsRange[m]))
        
        
        
    lines_labels = [axs[0].get_legend_handles_labels()]
    all_data = [np.random.normal(0, std, size=100) for std in range(1, 3)]
    #print(all_data)
    #print(type(all_data))
    axs[1].set_yticklabels([])
    axs[2].set_yticklabels([])
    
    if folder_name[k] == "sepsis":
        for n in range(len(epsRange)):
            axs[n].set_title(r'$\epsilon$ = ' + r'%s' % (epsRange[n]))
            
    if folder_name[k] != "traffic":
        for o in range(len(epsRange)):
            axs[o].set_xticklabels([])
    
    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
    colors = ['lightblue', 'pink']
    for bplot in (boxplots[0],boxplots[1],boxplots[2]):
        for patch, color in zip(bplot['boxes'], colors):
            patch.set_facecolor(color)
    #fig.legend(lines, labels,loc=1)
    #fig.legend(lines, ["DFG Approach","TVQ baseline"],loc=1)
    fig.set_size_inches(6, 3)
    img_name = folder_name[k]+'_'+ value_to_be_plotted +'.png'
    plt.subplots_adjust(left= 0.1,right=0.975,bottom=0.17,top=0.85,wspace=0.0)
    fig.savefig(img_name, dpi=300)
    
    #plt.show()
    
       