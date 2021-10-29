# Trace Variant Queries in Process Miningbased on Local Control-Flow Anonymization

This repository contains all of the code used in the Bachelor's thesis "Trace Variant Queries in Process Miningbased on Local Control-Flow Anonymization".

It also contains all the files necessary to evaluate and plot the figures and tables in the thesis.

## Requirements
You need various python packages to run this project
- Pandas (https://pandas.pydata.org/)
- NumPy (http://www.numpy.org)
- PM4Py (https://pm4py.fit.fraunhofer.de)
- OpyenXES (https://github.com/opyenxes/OpyenXes)




## Usage

1. Unzip logs in \\Logs folder

```python
call_local_control-flow_anon.py
```

Input:
1) file_name: Name of the log you want to sanitize
2) folder_name: Name of the folder that will be created in the \\Evaluation directory. Sanitized log and metadata will be saved here
3) epsilon_list: List of all epsilon value that the algorithm
4) tries: how often the algorithm is supposed to be execute and produce a sanitized event log for each e in epsilon_list

Output:
sanitized differentially private event log

*event log must be in .xes format and contain "concept:name"

## Evaluation Results

The scripts used for the creation of the figures and tables used in the thesis can be found in "Evaluation"

After executing call_local_control-flow_anon.py you finde some metadata here:
```python
\\Evaluation\\**folder_name**\\**folder_name**_stats.csv
\\Evaluation\\**folder_name**\\**folder_name**_trace_variant_distribution.csv
```

The code in the 'tvq' directory is based on the Trace Variant Query, the code of which can be found here:
 (https://github.com/samadeusfp/ELPaaS/tree/master/algorithms/laplace_tv)

The implementation of the inductive in Evaluation directory is based on the Evaluation used for the paper "SaCoFa: Semantics-aware Control-flow Anonymization for Process Mining",
 the code of which can be found here:
(https://github.com/samadeusfp/SaCoFa)



To plot figures you will first need to execute the Trace Variant Query baseline to compare the results to.
To do so, go to the tvq directy and execute:

```python
tvq.py
```


Input:(Choose the same as for call_local_control-flow_anon.py for consistenty)
1) file_name: Name of the log you want to sanitize
2) folder_name: Name of the folder that will be created in the \\Evaluation\\tvq directory. Sanitized log and metadata will be saved here
3) epsilon_list: List of all epsilon value that the algorithm,
4) tries: how often the algorithm is supposed to be execute and produce a sanitized event log for each e in epsilon_list

5) n: Maximum prefix of considered traces for the trace-variant-query. It must be an integer, N = 6 works well here
&) k: Prunning parameter of the trace-variant-query. At least k traces must appear in a noisy variant count to be part of the result of the query. It must be an integer, k = 4 works well here

This may take a while.

## Using the Inductive Miner
To be able to plot Fitness, Precision, Simplicity and generalization you first need to call the Inductive Miner
in the Evaluation directory
Choose (log_name, folder_name, original_log_path, epsRange, tries) accordingly
```python
call_model_quality_check.py
```

Choose (log_name, folder_name, epsRange, tries) accordingly
Then gather the data in a single .csv by calling and plot the data:

```python
Evaluationl\\pickle_to_csv.py
fitness_plot.py
```


The trace variant distribution can be plooted by calling
Choose (file_name, folder_name, epsRange, tries) accordingly
```python
tv_distribution_plot.py
```

Individual stats from all the **folder_name**_stats.csv can be compiled with:
```python
log_stats_to_csv_table.py
```



## Contact
oesinghf@hu-berlin.de

