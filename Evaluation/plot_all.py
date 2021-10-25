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

os.environ["PATH"] += os.pathsep + 'C:' + os.pathsep + 'users' + os.pathsep + 'oesinghaus' + os.pathsep + 'appdata' + os.pathsep + 'local' + os.pathsep + 'programs' + os.pathsep + 'python'+ os.pathsep + 'python36'+ os.pathsep + 'lib'+ os.pathsep + 'site-packages'+ os.pathsep + 'C:'

tries = 10
fig, axs = plt.subplots(1,len(epsRange))
fig.suptitle('Sepsis')

#DF_list = list()

#trace_variant_df.to_csv(os.path.join(new_folder_create_name,(folder_name + "_trace_variant_distribution.csv")))
#stats_dataframe.to_csv(os.path.join(new_folder_create_name,(folder_name + "_stats.csv")))


column_names = ['Log', 'dfg_approach eps = 0.01','dfg_approach eps = 0.1','dfg_approach eps = 1.0','pripel eps = 0.01','pripel eps = 0.1','pripel eps = 1.0']
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
    
    #print( "{0:.1f}".format(df_small_eps["runtime"].mean()))
    #sys.exit()
    #for k in range(len(epsRange)):
    result_df_runtime = result_df_runtime.append({'Log':folder_name[k], 'dfg_approach eps = 0.01': "{0:.1f}".format(df_small_eps["runtime"].mean()) ,'dfg_approach eps = 0.1': "{0:.1f}".format(df_medium_eps["runtime"].mean()),'dfg_approach eps = 1.0': "{0:.1f}".format(df_large_eps["runtime"].mean()),'pripel eps = 0.01': "{0:.1f}".format(df_pripel_small_eps["runtime"].mean()),'pripel eps = 0.1': "{0:.1f}".format(df_pripel_medium_eps["runtime"].mean()),'pripel eps = 1.0': "{0:.1f}".format(df_pripel_large_eps["runtime"].mean())}, ignore_index=True)
    #print("\n DF_list at eps =",epsRange[k])
    #print(DF_list[k])
    #axs[k].boxplot(sepsis_df[sepsis_df['epsilon'] == epsRange[k]])
    #axs[k].set_title(epsRange[k])
    #label =
    #axs[k].set_title(r'$\epsilon$ = ' + r'%s' % (epsRange[k]))
    #axs[k].xlabel("eps = ",epsRange[k])

result_df_runtime.to_csv("mean_runtime.csv")
sys.exit()

for i in range(len(epsRange)):
    anonymized_log_path = base_path + log_name + '_' + str(epsRange[k])  + '_' + str(i) + ".xes"
    result_path = base_path + log_name + '_' + str(epsRange[k]) + '_' + str(i) + ".pickle"

    df_dict = pd.read_pickle(result_path)

    #dict_list.append(df_dict)
    fitness = df_dict.pop("fitness", None)
    #print(fitness)
    df_dict['log_fitness'] = fitness.pop("log_fitness")
    df_dict['epsilon'] = epsRange[k]

    #print(df_dict)
    #print(DF_list[k])
    
    #df = pd.DataFrame([df_dict])
    f_score = (2.0 * df_dict.get('log_fitness') * df_dict.get('precision'))/(df_dict.get('log_fitness') + df_dict.get('precision'))
    df_dict['f_score'] = f_score
    #DF_list[k] = DF_list[k].append(df_dict,ignore_index=True)
    sepsis_df = sepsis_df.append(df_dict,ignore_index=True)
    
    #df.reset_index(drop=True, inplace=True)
    #pd.concat([DF_list[k], df],ignore_index=True)
    #print(df)
    #df = pd.DataFrame.from_dict(df_dict)
    #print(df_dict)
    #keys = df.keys()
    #values = df.values()

    #plt.bar(keys, values)
    #x = np.arange(0, 5, 0.1)
    #y = np.sin(x)
    #plt.plot(x, y)
    #plt.bar(range(len(df)), list(df.values()), align='center')
    #plt.xticks(range(len(df)), list(df.keys()))
    #plt.show()

for k in range(len(epsRange)):
    #print("\n DF_list at eps =",epsRange[k])
    #print(DF_list[k])
    axs[k].boxplot(sepsis_df[sepsis_df['epsilon'] == epsRange[k]])
    #axs[k].set_title(epsRange[k])
    #label =
    axs[k].set_title(r'$\epsilon$ = ' + r'%s' % (epsRange[k]))
    #axs[k].xlabel("eps = ",epsRange[k])

    
#df = pd.DataFrame(np.random.rand(10, 3), columns=['{:.2f}'.format(x) for x in epsRange])
#print(df)
#df.plot.box()
#plt.show()
#fig, axs = plt.subplots(2)
#fig.suptitle('Vertically stacked subplots')


#axs[0].boxplot(DF_list[0])
#axs[1].boxplot(DF_list[1])
#axs[2].boxplot(DF_list[2])

plt.show()