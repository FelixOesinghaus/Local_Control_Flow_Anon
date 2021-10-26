from pm4py.objects.log import log as event_log
from pm4py.objects.log import util as log_utils
from pm4py.objects.log.importer.xes import factory as xes_import_factory
from pm4py.objects.log.exporter.xes import factory as xes_exporter
from pm4py.objects.log.util import sampling
import tracematcher
from attributeAnonymizier import AttributeAnonymizier as AttributeAnonymizier
from trace_variant_query import privatize_tracevariants
import datetime
import sys
import pandas as pd
import sqlite3
import os
import time
from collections import Counter as Counter
from pathlib import Path
TRACE_START = "TRACE_START"
TRACE_END = "TRACE_END"
EVENT_DELIMETER = ">>>"
from dateutil.tz import tzutc
def freq(lst):
    d = {}
    for i in lst:
        if d.get(i):
            d[i] += 1
        else:
            d[i] = 1
    return d

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

def generate_pm4py_log_from_variants(trace_frequencies):
    log = event_log.EventLog()
    trace_count = 0
    for variant in trace_frequencies.items():
        frequency=variant[1]
        activities=variant[0].split(EVENT_DELIMETER)
        for i in range (0,frequency):
            trace = event_log.Trace()
            trace.attributes["concept:name"] = trace_count
            trace_count = trace_count + 1
            print(trace_count)
            for activity in activities:
                if not TRACE_END in activity:
                    event = event_log.Event()
                    event["concept:name"] = str(activity)
                    event["time:timestamp"] = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
                    trace.append(event)
            log.append(trace)
    return log

#file_name = "Sepsis_Cases_-_Event_Log.xes"
#file_name = "WABO_CoSeLoG_project.xes"
file_name = "Road_Traffic_Fine_Management_Process.xes"

#folder_name = "sepsis"
#folder_name = "coselog"
folder_name = "traffic"

logs_path = os.getcwd().replace("pripel", "Logs")
eval_path = os.path.join(os.getcwd().replace("pripel", "Evaluation"),"pripel")

new_folder_create_name = os.path.join(eval_path, folder_name)

filePath = os.path.join(logs_path,file_name)


epsilon = 0.1
N = 6
k = 4

log = xes_import_factory.apply(filePath)
#epsilon_list = [0.1, 1.0]
epsilon_list = [0.01,0.1,1.0]
tries = 10

column_names = ['epsilon','traces_before','traces_after','variants_before','variants_after','common_variants','runtime']
stats_dataframe = pd.DataFrame(columns = column_names)

prefix = get_prefix_frequencies_from_log(log)
traces_before = sum(prefix.values())
trace_variants = Counter(prefix)
most_common_tv_list = trace_variants.most_common(20)
common_traces_dict = dict(most_common_tv_list)
common_traces_dict['epsilon'] = 99.9
column_names_common_tv = list(common_traces_dict.keys())
trace_variant_df = pd.DataFrame(columns = column_names_common_tv)
trace_variant_df = trace_variant_df.append(common_traces_dict,ignore_index=True)
################################## pripel code

for i in range(len(epsilon_list)):
    for l in range(10):
        print(epsilon_list[i])
        start = time.time()
        #preprocess file
        #os.mkdir(secure_token)
        print("\n Starting privatize_df.py \n")
        #outpath_intermediate = filePath.replace('\\Logs','\\Evaluation\\placeholdernamexyz')
        #outpath_intermediate = outpath_intermediate.replace('placeholdernamexyz',folder_name)
        
        if Path.exists(Path(new_folder_create_name)):
            print("try : ",l," folder already exists")
        else:
            print("try : ",l," creating ", folder_name," folder")
            os.mkdir(new_folder_create_name)
        
        #outPath = outpath_intermediate.replace(".xes","_%s_%d.xes" % ((epsilon_list[i]),k))
        ##################
        new_ending = "_epsilon_" + str(epsilon_list[i])+ "_k" + str(l) + "_anonymizied.xes"
        output_file_name = file_name.replace(".xes", "_epsilon_" + str(epsilon_list[i])+ "_" + str(l) + "_laplace.xes")
        result_log_path_one = filePath.replace("\\Logs","\\Evaluation")
        result_log_path = result_log_path_one.replace(".xes",new_ending)

        print("\n output_path pripel: ",result_log_path,"\n")
        starttime = datetime.datetime.now()


        starttime_tv_query = datetime.datetime.now()
        tv_query_log, prefix, prefix_after_two = privatize_tracevariants(log, epsilon_list[i], k, N)
        prefix_after = get_prefix_frequencies_from_log(tv_query_log)
        private_log_from_variant = generate_pm4py_log_from_variants(prefix_after)
        print(len(tv_query_log))
        #endtime_tv_query = datetime.datetime.now()
        #print("Time of TV Query: " + str((endtime_tv_query - starttime_tv_query)))
        #print("print0")
        #starttime_trace_matcher = datetime.datetime.now()
        #print("print1")
        #traceMatcher = tracematcher.TraceMatcher(tv_query_log,log)
        #print("print2")
        #matchedLog = traceMatcher.matchQueryToLog()
        #print(len(matchedLog))
        #endtime_trace_matcher = datetime.datetime.now()
        #print("Time of TraceMatcher: " + str((endtime_trace_matcher - starttime_trace_matcher)))
        #distributionOfAttributes = traceMatcher.getAttributeDistribution()
        #occurredTimestamps, occurredTimestampDifferences = traceMatcher.getTimeStampData()
        #print(min(occurredTimestamps))
        #starttime_attribute_anonymizer = datetime.datetime.now()
        #attributeAnonymizier = AttributeAnonymizier()
        #anonymiziedLog, attritbuteDistribution = attributeAnonymizier.anonymize(matchedLog,distributionOfAttributes,epsilon_list[i],occurredTimestampDifferences,occurredTimestamps)
        #endtime_attribute_anonymizer = datetime.datetime.now()
        #print("Time of attribute anonymizer: " +str(endtime_attribute_anonymizer - starttime_attribute_anonymizer))
        #print(result_log_path)
        traces_after = sum(prefix_after.values())

        result_log_path = result_log_path.replace("\\",os.path.sep)#####

        #xes_exporter.export_log(private_log_from_variant, result_log_path)
        xes_exporter.export_log(private_log_from_variant, os.path.join(new_folder_create_name,output_file_name))
        endtime = datetime.datetime.now()
        appendable_to_common_variants = dict()
        
        for j in column_names_common_tv:
            appendable_to_common_variants[j] = prefix_after.get(j,0)
        appendable_to_common_variants['epsilon'] = epsilon_list[i]
        ####
        trace_variant_df = trace_variant_df.append(appendable_to_common_variants,ignore_index=True)
        end = time.time()
        comkeys = prefix.keys() & prefix_after.keys()
        stats_dataframe = stats_dataframe.append({'epsilon': epsilon_list[i],'traces_before': traces_before,'traces_after': traces_after,'variants_before': len(prefix.keys()),'variants_after': len(prefix_after.keys()),'common_variants': len(comkeys),'runtime': end-start }, ignore_index=True)
        
        print("Complete Time: " + str((endtime-starttime)))

        #print("Time of TV Query: " + str((endtime_tv_query - starttime_tv_query)))
        #print("Time of TraceMatcher: " + str((endtime_trace_matcher - starttime_trace_matcher)))
        #print("Time of attribute anonymizer: " +str(endtime_attribute_anonymizer - starttime_attribute_anonymizer))

        print(result_log_path)
        #print(freq(attritbuteDistribution))

        ######################################

trace_variant_df.to_csv(os.path.join(new_folder_create_name,(folder_name + "_trace_variant_distribution.csv")))
print(stats_dataframe)
stats_dataframe.to_csv(os.path.join(new_folder_create_name,(folder_name + "_stats.csv")))