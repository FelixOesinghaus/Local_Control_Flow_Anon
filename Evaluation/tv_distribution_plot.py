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


#base_path = os.getcwd() + os.sep + folder_name + os.sep

#os.environ["PATH"] += os.pathsep + 'C:' + os.pathsep + 'users' + os.pathsep + 'oesinghaus' + os.pathsep + 'appdata' + os.pathsep + 'local' + os.pathsep + 'programs' + os.pathsep + 'python'+ os.pathsep + 'python36'+ os.pathsep + 'lib'+ os.pathsep + 'site-packages'+ os.pathsep + 'C:'

tries = 10

for k in range(len(file_name)):
    fig, axs = plt.subplots(1,len(epsRange))
    
    if folder_name[k]=='sepsis':
        fig.suptitle('Sepsis trace variant frequencies')
    if folder_name[k]=='coselog':
        fig.suptitle('CoSeLog trace variant frequencies')
    if folder_name[k]=='traffic':
        fig.suptitle('Traffic Fines trace variant frequencies')
        
    DF_list = list()
    DF_list_tvq = list()

    #DF_list.append(pd.DataFrame(columns = column_names))
    #print(k)
    base_path = os.getcwd() + os.sep + folder_name[k] + os.sep
    base_path_tvq = os.getcwd() + os.sep +"tvq"+ os.sep + folder_name[k] + os.sep
    
    load_path = base_path + folder_name[k] + "_trace_variant_distribution.csv"
    load_path_tvq = base_path_tvq + folder_name[k] + "_trace_variant_distribution.csv"
    
    full_df = pd.read_csv(load_path, sep=',')
    full_df_tvq = pd.read_csv(load_path_tvq, sep=',')
    
    trace_names = full_df.columns.values.tolist()
    list_of_traces = trace_names[1:len(trace_names)-1]
    
    df_original = full_df[full_df['epsilon'] == 99.9]
    df_original = df_original.drop(["Unnamed: 0","epsilon"],axis=1)
    orig_values_list_of_lists = df_original.values.tolist()
    orig_values = orig_values_list_of_lists[0]
    
    one_to_twenty = list(range(1, 21))

    for m in range(len(epsRange)):
    
        DF_list.append(full_df[full_df['epsilon'] == epsRange[m]].drop(["Unnamed: 0","epsilon"],axis=1))
        DF_list_tvq.append(full_df_tvq[full_df_tvq['epsilon'] == epsRange[m]].drop(["Unnamed: 0","epsilon"],axis=1))
        plt.sca(axs[m])
        plt.grid(axis='y')
        plt.xticks(range(1,21))
        
        
        means = DF_list[m].mean(axis=0).tolist()
        tvq_means = DF_list_tvq[m].mean(axis=0).tolist()
        max = DF_list[m].max(axis=0).tolist()
        min = DF_list[m].min(axis=0).tolist()
        #print("\n DF_list at eps =",epsRange[k])
        #print(DF_list[k])
        #axs[k].boxplot(sepsis_df[sepsis_df['epsilon'] == epsRange[k]])
        #axs[k].set_title(epsRange[k])
        #label =
        axs[m].plot(one_to_twenty,tvq_means,color='black', linestyle='dashed',label="tvq baseline avg.")
        
        axs[m].plot(one_to_twenty,max,color='green', linestyle='dotted',label="Maximum occurrence")
        axs[m].plot(one_to_twenty,min,color='blue', linestyle='dotted',label="Minimum occurrence")
        axs[m].plot(one_to_twenty,means,color='red',label="Average occurrence")
        axs[m].scatter(one_to_twenty,orig_values,label="Original trace frequencies")
        
        
        axs[m].set_xlabel("20 most frequent trace variants")
        axs[m].set_ylabel("Frequency")
        axs[m].set_title(r'$\epsilon$ = ' + r'%s' % (epsRange[m]))
        
        
    lines_labels = [axs[0].get_legend_handles_labels()]

    lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]

    fig.legend(lines, labels,loc=1)
    fig.set_size_inches(13, 4)
    img_name = folder_name[k]+'_tv_freq.png'
    fig.savefig(img_name, dpi=300)

    #plt.show()
    
       