from check_model_quality import check_model_quality as check_model_quality
from generate_process_model import generate_process_model as generate_process_model
import sys
from pm4py.objects.log.importer.xes import importer as xes_importer
import os
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

## parameters
log_name = ["Sepsis_Cases_-_Event_Log","WABO_CoSeLoG_project","Road_Traffic_Fine_Management_Process"]
folder_name = ["sepsis","coselog","traffic"]
original_log_path = ['C:\\Users\\Oesinghaus\\Desktop\\Local_Control_Flow_Anon\Logs\\Sepsis_Cases_-_Event_Log.xes','C:\\Users\\Oesinghaus\\Desktop\\Local_Control_Flow_Anon\Logs\\WABO_CoSeLoG_project.xes','C:\\Users\\Oesinghaus\\Desktop\\Local_Control_Flow_Anon\Logs\\Road_Traffic_Fine_Management_Process.xes']
epsRange = [0.01, 0.1, 1.0]


#modeRange = ['occured','ba_prune']
#modeRange = ['laplace','ba_prune','occured','ba']


### Conformance Checking for DFG approach
for log_index in range(len(log_name)):

    base_path = os.getcwd() + os.sep + folder_name[log_index] + os.sep
    os.environ["PATH"] += os.pathsep + 'C:' + os.pathsep + 'users' + os.pathsep + 'oesinghaus' + os.pathsep + 'appdata' + os.pathsep + 'local' + os.pathsep + 'programs' + os.pathsep + 'python'+ os.pathsep + 'python36'+ os.pathsep + 'lib'+ os.pathsep + 'site-packages'+ os.pathsep + 'C:'

    original_log = xes_importer.apply(original_log_path[log_index])
    tries = 10
    for eps in epsRange:
        for i in range(tries):

            anonymized_log_path = base_path + log_name[log_index] + '_' + str(eps)  + '_' + str(i) + ".xes"
            anonymized_log = xes_importer.apply(anonymized_log_path)
            result_path = base_path + log_name[log_index] + '_' + str(eps) + '_' + str(i) + ".pickle"
            check_model_quality(original_log=original_log,anonymized_log=anonymized_log,result_path=result_path)
            generate_process_model(anonymized_log_path,result_path)
            


### Conformance Checking for Trace Variant Query
for log_index in range(len(log_name)):

    base_path = os.getcwd() + os.sep + "tvq" + os.sep + folder_name[log_index] + os.sep
    os.environ["PATH"] += os.pathsep + 'C:' + os.pathsep + 'users' + os.pathsep + 'oesinghaus' + os.pathsep + 'appdata' + os.pathsep + 'local' + os.pathsep + 'programs' + os.pathsep + 'python'+ os.pathsep + 'python36'+ os.pathsep + 'lib'+ os.pathsep + 'site-packages'+ os.pathsep + 'C:'

    original_log = xes_importer.apply(original_log_path[log_index])
    tries = 10
    for eps in epsRange:
        for i in range(0,1):

            anonymized_log_path = base_path + log_name[log_index] + '_epsilon' + '_' + str(eps)  + '_' + str(i) + "_laplace.xes"
            anonymized_log = xes_importer.apply(anonymized_log_path)
            result_path = base_path + log_name[log_index] + '_' + str(eps) + '_' + str(i) + ".pickle"
            check_model_quality(original_log=original_log,anonymized_log=anonymized_log,result_path=result_path)
            generate_process_model(anonymized_log_path,result_path)
            
