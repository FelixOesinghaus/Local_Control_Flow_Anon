import matplotlib.pyplot as plt
import sys
import sqlite3
import os
import subprocess
import requests
import time
import urllib3
import shutil
import glob
from tabulate import tabulate
import pathlib
from pathlib import Path
from opyenxes.classification.XEventNameClassifier import XEventNameClassifier
from opyenxes.data_in.XUniversalParser import XUniversalParser
#import opyenxes.factory.XFactory as xfactory
import numpy as np
import pandas as pd
from pm4py.objects.log import log as event_log
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log import util as log_utils
from pm4py.objects.log.exporter.xes import factory as xes_exporter
import random
import datetime
from dateutil.tz import tzutc
from collections import Counter as Counter


TRACE_START = "TRACE_START"
TRACE_END = "TRACE_END"
EVENT_DELIMETER = ">>>"

sys.setrecursionlimit(1000)

def privatize_df(log, event_int_mapping, epsilon, output):
    #get true df frequencies
    print("Retrieving Directly Follows Frequencies   ", end = '')
    df_relations = get_df_frequencies(log, event_int_mapping)
    
    traces_before = np.sum(df_relations[0])
    print("\n Traces before noise:", np.sum(df_relations[0]),"\n")
    
    print("Done")
    #privatize df frequencies
    print("Privatizing Log   ", end = '')
    int_event_mapping = {value:key for key, value in event_int_mapping.items()}
    #print(int_event_mapping)
    activity_list = []
    for key, value in int_event_mapping.items():
        temp = [key,value]
        activity_list.append(value)
    
    #df = pd.DataFrame(data=df_relations, index=activity_list, columns=activity_list)
    #df.to_csv('df_relations.csv',sep=',',columns=activity_list, header=activity_list)
    df_relations = apply_laplace_noise_df(df_relations, epsilon)
    print("Done")
    
    #write to disk
    print("Writing privatized Directly Follows Frequencies to disk   ","\n")
    #write_to_dfg(df_relations, event_int_mapping, output)
    private_log, counter, total_df_amount, total_df_deleted = generate_pm4py_log(df_relations, event_int_mapping,int_event_mapping, activity_list)
    ##############xes_exporter.export_log(private_log,output)
    print("Done")
    return private_log, traces_before, counter, total_df_amount, total_df_deleted

def create_event_int_mapping(log):
    event_name_list=[]
    #print("\n log type:",type(log))
    for trace in log:
        #print("trace type:",type(trace))
        for event in trace:
            #print("event type:",type(event), event)
            event_name = event["concept:name"]
            if not str(event_name) in event_name_list:
                event_name_list.append(event_name)
    event_int_mapping={}
    event_int_mapping[TRACE_START]=0
    current_int=1
    for event_name in event_name_list:
        event_int_mapping[event_name]=current_int
        current_int=current_int+1
    event_int_mapping[TRACE_END]=current_int
    #print("\n",type(event_int_mapping)," \n",event_int_mapping,"\n \n")
    return event_int_mapping

def get_df_frequencies(log, event_int_mapping):
    classifier = XEventNameClassifier()
    df_relations = np.zeros((len(event_int_mapping),len(event_int_mapping)), dtype=int)
    for trace in log[0]:
        current_event = TRACE_START
        for event in trace:
            next_event = classifier.get_class_identity(event)
            current_event_int = event_int_mapping[current_event]
            next_event_int = event_int_mapping[next_event]
            df_relations[current_event_int, next_event_int] += 1
            current_event = next_event
        
        current_event_int = event_int_mapping[current_event]
        next_event = TRACE_END
        next_event_int = event_int_mapping[next_event]
        df_relations[current_event_int, next_event_int] += 1
        
    
    return df_relations

def apply_laplace_noise_df(df_relations, epsilon):
    lambd = 1/float(epsilon)
    size = df_relations.shape[0]
    #print("\n",size,"\n")
    for i in range(size):
        for k in range(size):
            noise = int(np.random.laplace(0, lambd))
            df_relations[i,k] = df_relations[i,k] + noise
            if df_relations[i,k]<0:
                df_relations[i,k]=0
    
    df_relations[:,0] = 0
    df_relations[0,size-1] = 0
    df_relations[size-1] = 0
    #print(df_relations)
    return df_relations

def write_to_dfg(df_relations, event_int_mapping, output):
    out=output+".dfg"
    print("\n output_path: ",out,"\n")
    f = open(out,"w+")
    f.write(str(len(df_relations)-2)+"\n")
    for key in event_int_mapping:
        if not (str(key)==TRACE_START or str(key)==TRACE_END):
            f.write(str(key)+"\n")

    #starting activities
    no_starting_activities=0
    starting_frequencies=[]
    for x in range(1,len(df_relations)):
        current = df_relations[0,x]
        if current!=0:
            no_starting_activities+=1
            starting_frequencies.append((x-1,current))
    f.write(str(no_starting_activities)+"\n")
    for x in starting_frequencies:
        f.write(str(x[0])+"x"+str(x[1])+"\n")

    #ending activities
    no_ending_activities=0
    ending_frequencies=[]
    for x in range(0,len(df_relations)-1):
        current = df_relations[x,len(df_relations)-1]
        if current!=0:
            no_ending_activities+=1
            ending_frequencies.append((x-1, current))
    f.write(str(no_ending_activities)+"\n")
    for x in ending_frequencies:
        f.write((str(x[0])+"x"+str(x[1])+"\n"))

    #df relations
    for x in range(1,len(df_relations)-1):
        for y in range(1,len(df_relations)-1):
            if df_relations[x,y]!=0:
                f.write(str(x-1)+">"+str(y-1)+"x"+str(df_relations[x,y])+"\n")
    f.close

def find_path(df_relations,deleted_df,activity_list,possible_elements,existing_path,depth):
    
    current_activity = existing_path[-1]
    full_trace = False
    if current_activity == df_relations.shape[0]-1:
        full_trace = True
    if full_trace==False:
        if np.sum(df_relations[current_activity]) > 0:
            
            ###statistic choice
            probabilities_current_df = df_relations[current_activity] / np.sum(df_relations[current_activity])
            
            ###equeal probability
            #probabilities_current_df = np.clip(df_relations[current_activity], 0, 1)* (1/np.count_nonzero(df_relations[current_activity]))
            ###
            next_activity = np.random.choice(possible_elements,p=probabilities_current_df)
            existing_path.append(next_activity)
            if df_relations[existing_path[-2],existing_path[-1]] > 0:
                df_relations[existing_path[-2],existing_path[-1]] -= 1
            depth += 1
            if depth == 500:
                print("depth over 500",existing_path)
                print(df_relations)
                return [0]
            existing_path=find_path(df_relations,deleted_df,activity_list,possible_elements,existing_path,depth)
        else:
            deleted_df[:,existing_path[-1]] = df_relations[:,existing_path[-1]]
            #print(df_relations,"\n")
            #print(deleted_df,"\n")
            
            #df = pd.DataFrame(data=df_relations, index=activity_list, columns=activity_list)
            #df.to_csv('df_relation_end.csv',sep=',',columns=activity_list, header=activity_list)
            
            #df = pd.DataFrame(data=deleted_df, index=activity_list, columns=activity_list)
            #df.to_csv('df_deletions_end.csv',sep=',',columns=activity_list, header=activity_list)
            
            #df = pd.DataFrame(data=df_relations, index=activity_list, columns=activity_list)
            #df.to_csv('df_relations_noised.csv',sep=',',columns=activity_list, header=activity_list)
            #sys.exit()
            if current_activity == 0:
                print("No more viable paths to TRACE_END")
                return [0]
            depth += 1
            df_relations[:,existing_path[-1]] = 0            
            existing_path = existing_path[:-1]
            existing_path = find_path(df_relations,deleted_df,activity_list,possible_elements,existing_path,depth) 
            
            
    return existing_path
 
def generate_pm4py_log(df_relations, event_int_mapping,int_event_mapping, activity_list):
    #int_event_mapping = {value:key for key, value in event_int_mapping.items()}
    #print(int_event_mapping)
    
    log = event_log.EventLog()
    size = df_relations.shape[0]-1
    print("START:",np.sum(df_relations[0]),np.sum(df_relations,axis=0)[size],"\n\n")
    trace_amount = min(np.sum(df_relations[0]),np.sum(df_relations,axis=0)[size])
    possible_elements = list(range(0,size+1))#counter < trace_amount
    total_df_amount = df_relations.sum()
    deleted_df = np.zeros((len(int_event_mapping),len(int_event_mapping)), dtype=int)
    new_df_amount = df_relations.sum()
    
    #df = pd.DataFrame(data=df_relations, index=activity_list, columns=activity_list)
    #df.to_csv('df_relations_noised.csv',sep=',',columns=activity_list, header=activity_list)
    
    #print(tabulate(df, headers= activity_list,tablefmt = 'pretty'))
    #plt.matshow(df_relations,fignum=None,cmap='gray')
    #plt.savefig('df_relations.png',dpi=300)
    #print("hello?")
    #sys.exit()
    counter = 0
    while(True):
        empty_list=[0]
        old_df_amount = new_df_amount
        next_trace = find_path(df_relations,deleted_df,activity_list,possible_elements ,empty_list,0)
        new_df_amount = df_relations.sum()
        
        #print("trace nr.: ",counter,next_trace,"lentgh:",len(next_trace))
        #print("total dfs - current trace:", old_df_amount - new_df_amount)
            
        #if old_df_amount - new_df_amount != len(next_trace) -1:
        #    print("weird deletion")
        #sys.exit()
        if len(next_trace) <= 1:
            print("All traces attached to log.", counter, "traces")
            break
        
        trace = event_log.Trace()
        trace.attributes["concept:name"] = counter
        counter += 1
        
        
        for i in range(len(next_trace)-1):
            #print(df_relations[next_trace[i],next_trace[i+1]])
            #if df_relations[next_trace[i],next_trace[i+1]] > 0:
            #    df_relations[next_trace[i],next_trace[i+1]] -= 1
            if str(int_event_mapping[next_trace[i]]) == TRACE_START:
                continue
            event = event_log.Event()
            event["concept:name"] = str(int_event_mapping[next_trace[i]])
            event["time:timestamp"] = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
            trace.append(event)
        
        log.append(trace)
        #print("appended:" ,counter, next_trace) 
    
    #print(df_relations,"\n")
    #print("deleted df:\n",deleted_df,"\n")
    
    #df = pd.DataFrame(data=df_relations, index=activity_list, columns=activity_list)
    #df.to_csv('df_relation_end.csv',sep=',',columns=activity_list, header=activity_list)
    
    df_deletions = np.add(deleted_df,df_relations)
    #print(df_deletions,"\n")
    
    #df = pd.DataFrame(data=df_deletions, index=activity_list, columns=activity_list)
    #df.to_csv('df_deletions_end.csv',sep=',',columns=activity_list, header=activity_list)
    
    total_df_deleted = df_deletions.sum()
    print("total cases:",counter)
    print("Total df relations:",total_df_amount,"total deletions:",total_df_deleted," Percentage deleted =", total_df_deleted / total_df_amount)
    return log, counter, total_df_amount, total_df_deleted

def get_prefix_frequencies_from_log(log):
        prefix_frequencies = {}
        for trace in log:
            current_prefix = ""
            for event in trace:
                #current_prefix = current_prefix + event["concept:name"] + EVENT_DELIMETER
                current_prefix = current_prefix + event["concept:name"] + EVENT_DELIMETER
                #if current_prefix in prefix_frequencies:
                #    frequency = prefix_frequencies[current_prefix]
                #    prefix_frequencies[current_prefix] += 1
                #else:
                #    prefix_frequencies[current_prefix] = 1
            current_prefix = current_prefix + TRACE_END
            #prefix_frequencies[current_prefix] = 1
            if current_prefix in prefix_frequencies:
                frequency = prefix_frequencies[current_prefix]
                prefix_frequencies[current_prefix] += 1
            else:
                prefix_frequencies[current_prefix] = 1
        return prefix_frequencies


#file_name = "Sepsis_Cases_-_Event_Log.xes"
file_name = "WABO_CoSeLoG_project.xes"
#file_name = "Road_Traffic_Fine_Management_Process.xes"

#folder_name = "sepsis"
folder_name = "coselog"
#folder_name = "traffic"

filePath = os.path.join(os.getcwd(),"Logs",file_name)
new_folder_create_name = os.path.join(os.getcwd(),"Evaluation", folder_name)

log = xes_import_factory.apply(filePath)
parser = XUniversalParser()

if parser.can_parse(filePath):
    print("log can be parsed.")
else:
    print("log can not be parsed.")

log_file = open(filePath)
log_list = parser.parse(log_file)

epsilon_list = [0.01, 0.1, 1.0]
tries = 10

column_names = ['epsilon','traces_before','traces_after','total_df_amount','total_df_deleted','df_percentage deleted','variants_before','variants_after','common_variants','runtime']
stats_dataframe = pd.DataFrame(columns = column_names)

prefix = get_prefix_frequencies_from_log(log)


#with open('pre_DFG.txt', 'w') as f:
#    for key, value in prefix.items():
#        print(key,value, file=f)


event_mapping = create_event_int_mapping(log)

trace_variants = Counter(prefix)
most_common_tv_list = trace_variants.most_common(20)

common_traces_dict = dict(most_common_tv_list)
common_traces_dict['epsilon'] = 99.9

column_names_common_tv = list(common_traces_dict.keys())

trace_variant_df = pd.DataFrame(columns = column_names_common_tv)

trace_variant_df = trace_variant_df.append(common_traces_dict,ignore_index=True)


for i in range(len(epsilon_list)):
    for k in range(tries):
        print(epsilon_list[i])
        start = time.time()
        #preprocess file
        #os.mkdir(secure_token)
        print("\n Starting privatize_df.py \n")
        outpath_intermediate = filePath.replace('\\Logs','\\Evaluation\\placeholdernamexyz')
        outpath_intermediate = outpath_intermediate.replace('placeholdernamexyz',folder_name)
        
        if Path.exists(Path(new_folder_create_name)):
            print("try : ",k," folder already exists")
        else:
            print("try : ",k," creating ", folder_name," folder")
            os.mkdir(new_folder_create_name)
        
        outPath = outpath_intermediate.replace(".xes","_%s_%d.xes" % ((epsilon_list[i]),k))


        
        
        private_log,traces_before, traces_after, total_df_amount, total_df_deleted = privatize_df(log_list, event_mapping, (epsilon_list[i]), outPath)
        df_percentage_deleted = total_df_deleted / total_df_amount
        
        xes_exporter.export_log(private_log,outPath)
        end = time.time()
        print("Time : ", end-start)
        prefix_after = get_prefix_frequencies_from_log(private_log)
        #with open('post_DFG_%s.txt'%(epsilon_list[i]), 'w') as f:
        #    for key, value in prefix_after.items():
        #        print(key,value, file=f)
                
        ###
        appendable_to_common_variants = dict()
        
        for j in column_names_common_tv:
            appendable_to_common_variants[j] = prefix_after.get(j,0)
        appendable_to_common_variants['epsilon'] = epsilon_list[i]
        ####
        trace_variant_df = trace_variant_df.append(appendable_to_common_variants,ignore_index=True)
        
        comkeys = prefix.keys() & prefix_after.keys()
        stats_dataframe = stats_dataframe.append({'epsilon': epsilon_list[i],'traces_before': traces_before,'traces_after': traces_after,'total_df_amount': total_df_amount,'total_df_deleted': total_df_deleted,'df_percentage deleted': df_percentage_deleted,'variants_before': len(prefix.keys()),'variants_after': len(prefix_after.keys()),'common_variants': len(comkeys),'runtime': end-start }, ignore_index=True)
        
#write to db
#print("Writing to DB")
#print(outPath)
#puffer,targetFile = outPath.split("media"+os.path.sep)

trace_variant_df.to_csv(os.path.join(new_folder_create_name,(folder_name + "_trace_variant_distribution.csv")))
print(stats_dataframe)
stats_dataframe.to_csv(os.path.join(new_folder_create_name,(folder_name + "_stats.csv")))