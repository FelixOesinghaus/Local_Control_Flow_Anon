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


log_name = ["Sepsis_Cases_-_Event_Log","WABO_CoSeLoG_project","Road_Traffic_Fine_Management_Process"]
folder_name = ["sepsis","coselog","traffic"]


epsRange = [0.01, 0.1, 1.0]
#modeRange = ['occured','ba_prune']
#modeRange = ['laplace','ba_prune','occured','ba']

tries = 10

column_names = ['epsilon', 'precision','generalization','simplicity','log_fitness','f_score']

for k in range(len(log_name)):

    base_path = os.getcwd() + os.sep + folder_name[k] + os.sep
    base_path_tvq = os.getcwd() + os.sep + "tvq" + os.sep + folder_name[k] + os.sep
    
    dfg_df = pd.DataFrame(columns = column_names)
    tvq_df = pd.DataFrame(columns = column_names)

    for m in range(len(epsRange)):
        
        for i in range(tries):
            anonymized_log_path = base_path + log_name[k] + '_' + str(epsRange[m])  + '_' + str(i) + ".xes"
            
            result_path = base_path + log_name[k] + '_' + str(epsRange[m]) + '_' + str(i) + ".pickle"
            result_path_tvq = base_path_tvq + log_name[k] + '_' + str(epsRange[m]) + '_' + str(i) + ".pickle"
            
            df_dict = pd.read_pickle(result_path)
            df_dict_tvq = pd.read_pickle(result_path_tvq)

            
            fitness = df_dict.pop("fitness", None)
            
            df_dict['log_fitness'] = fitness.pop("log_fitness")
            df_dict['epsilon'] = epsRange[m]
            
            fitness_tvq = df_dict_tvq.pop("fitness", None)
            
            df_dict_tvq['log_fitness'] = fitness_tvq.pop("log_fitness")
            df_dict_tvq['epsilon'] = epsRange[m]
            
            f_score = (2.0 * df_dict.get('log_fitness') * df_dict.get('precision'))/(df_dict.get('log_fitness') + df_dict.get('precision'))
            df_dict['f_score'] = f_score
            
            f_score_tvq = (2.0 * df_dict_tvq.get('log_fitness') * df_dict_tvq.get('precision'))/(df_dict_tvq.get('log_fitness') + df_dict_tvq.get('precision'))
            df_dict_tvq['f_score'] = f_score_tvq
            
            dfg_df = dfg_df.append(df_dict,ignore_index=True)
            tvq_df = tvq_df.append(df_dict_tvq,ignore_index=True)
            
            
            
            
    dfg_df.to_csv(base_path + folder_name[k] + "_fitness.csv")
    tvq_df.to_csv(base_path_tvq + folder_name[k] + "_fitness.csv")
    

