import os
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.objects.conversion.process_tree import converter as pt_converter
import pm4py

#C:\users\oesinghaus\appdata\local\programs\python\python36\lib\site-packages
import os

path = 'C:\\Users\\Oesinghaus\\Desktop\\df\\miner\\'
os.environ["PATH"] += os.pathsep + 'C:' + os.pathsep + 'users' + os.pathsep + 'oesinghaus' + os.pathsep + 'appdata' + os.pathsep + 'local' + os.pathsep + 'programs' + os.pathsep + 'python'+ os.pathsep + 'python36'+ os.pathsep + 'lib'+ os.pathsep + 'site-packages'+ os.pathsep + 'C:'
#file_path = 'C:\\Users\\Oesinghaus\\Desktop\\df\\miner\\Sepsis_Cases_-_Event_Log_0.1.xes'
#file_path = 'Sepsis_Cases_-_Event_Log_0.1.xes'
file_path = 'Sepsis_Cases_-_Event_Log.xes'
log = xes_importer.apply(file_path)
net, initial_marking, final_marking = inductive_miner.apply(log)
net_file_path = 'C:\\Users\\Oesinghaus\\Desktop\\df\\miner\\net2.png'

net_file_path_two = path + file_path.replace(".xes","_net.png")
print(net_file_path)
print(net_file_path_two)
#tree = inductive_miner.apply_tree(log)

#gviz = pt_visualizer.apply(tree)
#pt_visualizer.view(gviz)

#net, initial_marking, final_marking = pt_converter.apply(tree, variant=pt_converter.Variants.TO_PETRI_NET)
pm4py.save_vis_petri_net(net, initial_marking, final_marking, net_file_path)
