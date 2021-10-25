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



tries = 10
fig, axs = plt.subplots(1,len(epsRange))
fig.suptitle('Sepsis')

#DF_list = list()

#trace_variant_df.to_csv(os.path.join(new_folder_create_name,(folder_name + "_trace_variant_distribution.csv")))
#stats_dataframe.to_csv(os.path.join(new_folder_create_name,(folder_name + "_stats.csv")))


#column_names = ['Log', 'dfg_approach eps = 0.01','dfg_approach eps = 0.1','dfg_approach eps = 1.0','pripel eps = 0.01','pripel eps = 0.1','pripel eps = 1.0']
#column_names = ['Log','traces_before', 'dfg_approach eps = 0.01','dfg_approach eps = 0.1','dfg_approach eps = 1.0','pripel eps = 0.01','pripel eps = 0.1','pripel eps = 1.0']
#column_names = ['Log','total_df_amount', 'total_df_deletedeps = 0.01','total_df_deletedeps = 0.1','total_df_deletedeps = 1.00','df_percentage deleted eps = 0.01','df_percentage deleted eps = 0.1','df_percentage deleted eps = 1.00']
#column_names = ['Log','variants_before', 'total_df_deletedeps = 0.01','total_df_deletedeps = 0.1','total_df_deletedeps = 1.00','df_percentage deleted eps = 0.01','df_percentage deleted eps = 0.1','df_percentage deleted eps = 1.00']
column_names = ['Log','variants_before', 'variants eps = 0.01','variants eps = 0.1','variants eps = 1.00','variants pripel eps = 0.01','variants pripel eps = 0.1','variants pripel eps = 1.00']
result_df_runtime = pd.DataFrame(columns = column_names)

#for k in range(len(epsRange)):
for k in range(len(file_name)):
    #DF_list.append(pd.DataFrame(columns = column_names))
    #print(k)
    base_path = os.getcwd() + os.sep + folder_name[k] + os.sep
    base_path_pripel = os.getcwd() + os.sep +"pripel"+ os.sep + folder_name[k] + os.sep
    
    load_path = base_path + folder_name[k] + "_stats.csv"
    load_path_pripel = base_path_pripel + folder_name[k] + "_stats.csv"
    
    full_df = pd.read_csv(load_path, sep=',')
    full_df_pripel = pd.read_csv(load_path_pripel, sep=',')
    
    df_small_eps = full_df[full_df['epsilon'] == epsRange[0]]
    df_medium_eps = full_df[full_df['epsilon'] == epsRange[1]]
    df_large_eps = full_df[full_df['epsilon'] == epsRange[2]]
    
    
    
    df_pripel_small_eps = full_df_pripel[full_df_pripel['epsilon'] == epsRange[0]]
    df_pripel_medium_eps = full_df_pripel[full_df_pripel['epsilon'] == epsRange[1]]
    df_pripel_large_eps = full_df_pripel[full_df_pripel['epsilon'] == epsRange[2]]
    
    #traces_before = df_small_eps["traces_before"].mean()
    #total_df = df_small_eps["total_df_amount"].mean()
    variants_before = "{0:.0f}".format(df_small_eps["variants_before"].mean())
    
    #small_eps_dfg_value = "{0:.0f}".format(df_small_eps["variants_after"].min()) + " - " + "{0:.0f}".format(df_small_eps["variants_after"].max()) 
    #medium_eps_dfg_value = "{0:.0f}".format(df_medium_eps["variants_after"].min()) + " - " + "{0:.0f}".format(df_medium_eps["variants_after"].max())
    #large_eps_dfg_value = "{0:.0f}".format(df_large_eps["variants_after"].min()) + " - " + "{0:.0f}".format(df_large_eps["variants_after"].max()) 
    
    small_eps_dfg_value = "{0:.0f}".format(df_small_eps["common_variants"].min()) + " - " + "{0:.0f}".format(df_small_eps["common_variants"].max()) 
    medium_eps_dfg_value = "{0:.0f}".format(df_medium_eps["common_variants"].min()) + " - " + "{0:.0f}".format(df_medium_eps["common_variants"].max())
    large_eps_dfg_value = "{0:.0f}".format(df_large_eps["common_variants"].min()) + " - " + "{0:.0f}".format(df_large_eps["common_variants"].max()) 
    
    #small_eps_dfg_value = "{0:.2f}".format((df_small_eps["traces_after"].min()/traces_before)) 
    #medium_eps_dfg_value = "{0:.2f}".format((df_medium_eps["traces_after"].min()/traces_before))
    #large_eps_dfg_value = "{0:.2f}".format((df_large_eps["traces_after"].min()/traces_before)) 
    
    #small_eps_dfg_value = "{0:.0f}".format((df_small_eps["total_df_deleted"].mean())) 
    #medium_eps_dfg_value = "{0:.0f}".format((df_medium_eps["total_df_deleted"].mean()))
    #large_eps_dfg_value = "{0:.0f}".format((df_large_eps["total_df_deleted"].mean())) 
    
    
    #small_eps_pripel_value = "{0:.2f}".format((df_pripel_small_eps["traces_after"].min()/traces_before)) + "-" + "{0:.2f}".format((df_pripel_small_eps["traces_after"].max()/traces_before)) 
    #medium_eps_pripel_value = "{0:.2f}".format((df_pripel_medium_eps["traces_after"].min()/traces_before)) + "-" + "{0:.2f}".format((df_pripel_medium_eps["traces_after"].max()/traces_before)) 
    #large_eps_pripel_value = "{0:.2f}".format((df_pripel_large_eps["traces_after"].min()/traces_before)) + "-" + "{0:.2f}".format((df_pripel_large_eps["traces_after"].max()/traces_before)) 
    #small_eps_pripel_value = "{0:.0f}".format(df_pripel_small_eps["variants_after"].min()) + " - " + "{0:.0f}".format(df_pripel_small_eps["variants_after"].max()) 
    #medium_eps_pripel_value = "{0:.0f}".format(df_pripel_medium_eps["variants_after"].min()) + " - " + "{0:.0f}".format(df_pripel_medium_eps["variants_after"].max()) 
    #large_eps_pripel_value = "{0:.0f}".format(df_pripel_large_eps["variants_after"].min()) + " - " + "{0:.0f}".format(df_pripel_large_eps["variants_after"].max()) 
    
    small_eps_pripel_value = "{0:.0f}".format(df_pripel_small_eps["common_variants"].min()) + " - " + "{0:.0f}".format(df_pripel_small_eps["common_variants"].max()) 
    medium_eps_pripel_value = "{0:.0f}".format(df_pripel_medium_eps["common_variants"].min()) + " - " + "{0:.0f}".format(df_pripel_medium_eps["common_variants"].max()) 
    large_eps_pripel_value = "{0:.0f}".format(df_pripel_large_eps["common_variants"].min()) + " - " + "{0:.0f}".format(df_pripel_large_eps["common_variants"].max()) 
    
    
    #print( "{0:.1f}".format(df_small_eps["runtime"].mean()))
    #sys.exit()
    #for k in range(len(epsRange)):
    #runtime
    #result_df_runtime = result_df_runtime.append({'Log':folder_name[k], 'dfg_approach eps = 0.01': "{0:.1f}".format(df_small_eps["runtime"].mean()) ,'dfg_approach eps = 0.1': "{0:.1f}".format(df_medium_eps["runtime"].mean()),'dfg_approach eps = 1.0': "{0:.1f}".format(df_large_eps["runtime"].mean()),'pripel eps = 0.01': "{0:.1f}".format(df_pripel_small_eps["runtime"].mean()),'pripel eps = 0.1': "{0:.1f}".format(df_pripel_medium_eps["runtime"].mean()),'pripel eps = 1.0': "{0:.1f}".format(df_pripel_large_eps["runtime"].mean())}, ignore_index=True)
    traces_before = df_small_eps["traces_before"].mean()
    #result_df_runtime = result_df_runtime.append({'Log':folder_name[k],'traces_before': "{0:.0f}".format(df_small_eps["traces_before"].mean()) , 'dfg_approach eps = 0.01': "{0:.0f}".format(df_small_eps["traces_after"].mean()) ,'dfg_approach eps = 0.1': "{0:.0f}".format(df_medium_eps["traces_after"].mean()),'dfg_approach eps = 1.0': "{0:.0f}".format(df_large_eps["traces_after"].mean()),'pripel eps = 0.01': "{0:.0f}".format(df_pripel_small_eps["traces_after"].mean()),'pripel eps = 0.1': "{0:.0f}".format(df_pripel_medium_eps["traces_after"].mean()),'pripel eps = 1.0': "{0:.0f}".format(df_pripel_large_eps["traces_after"].mean())}, ignore_index=True)
    #result_df_runtime = result_df_runtime.append({'Log':folder_name[k],'traces_before': "{0:.0f}".format(df_small_eps["traces_before"].mean()) , 'dfg_approach eps = 0.01': small_eps_dfg_value ,'dfg_approach eps = 0.1': medium_eps_dfg_value,'dfg_approach eps = 1.0': large_eps_dfg_value,'pripel eps = 0.01': small_eps_pripel_value,'pripel eps = 0.1': medium_eps_pripel_value,'pripel eps = 1.0': large_eps_pripel_value}, ignore_index=True)
    result_df_runtime = result_df_runtime.append({'Log':folder_name[k],'variants_before':variants_before, 'variants eps = 0.01':small_eps_dfg_value,'variants eps = 0.1':medium_eps_dfg_value,'variants eps = 1.00':large_eps_dfg_value,'variants pripel eps = 0.01':small_eps_pripel_value,'variants pripel eps = 0.1':medium_eps_pripel_value,'variants pripel eps = 1.00': large_eps_pripel_value}, ignore_index=True)
    
    #print("\n DF_list at eps =",epsRange[k])
    #print(DF_list[k])
    #axs[k].boxplot(sepsis_df[sepsis_df['epsilon'] == epsRange[k]])
    #axs[k].set_title(epsRange[k])
    #label =
    #axs[k].set_title(r'$\epsilon$ = ' + r'%s' % (epsRange[k]))
    #axs[k].xlabel("eps = ",epsRange[k])

#result_df_runtime.to_csv("mean_runtime.csv")
#result_df_runtime.to_csv("mean_traces_percent.csv")
#result_df_runtime.to_csv("mean_dfg.csv")
#result_df_runtime.to_csv("variants_dfg_pripel.csv")
result_df_runtime.to_csv("common_variants.csv")
