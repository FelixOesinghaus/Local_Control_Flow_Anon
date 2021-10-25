import sys
import pandas as pd
import pickle
import os

log_name = sys.argv[1]
base_path = sys.argv[2]
result_dir_path = sys.argv[3]

epsRange = [0.01, 0.1, 1.0]
tries = 10                                                          # how many tries per epsilon       for i in range(tries):

df = pd.DataFrame()
result_file_path = os.path.join(result_dir_path, log_name + "_results.csv")


for eps in epsRange:

    file_path = os.path.join(base_path, log_name + '_' + str(eps) + '_' + str(0) + ".pickle")
    if os.path.exists(file_path):
        data = dict()
        file = open(file_path, 'rb')
        data_results = pickle.load(file)
        data["log_name"] = log_name
        data["run"] = 0
        data["epsilon"] = eps
        data["precision"] = data_results["precision"]
        data["simplicity"] = data_results["simplicity"]
        data["generalization"] = data_results["generalization"]
        data["fitness"] = data_results["fitness"]["average_trace_fitness"]
        data["fit_traces"] = data_results["fitness"]["perc_fit_traces"]
        df = df.append(data,ignore_index=True)
df.to_csv(result_file_path,index=False,sep=';')