import os
import sys
import random
import numpy as np
from collections import OrderedDict
import operator
import sys
import json
from collections import Counter

#delete node 0,delete vertex 1,modifyweight 2,add nvertex 3 ,add node 4

class Operation:
    def __init__(self,fileid,mode,operation):
        self.fileid = fileid
        self.mode = mode
        self.operation = operation 
    
    def __repr__(self):
        return repr((self.fileid,self.mode,self.operation))
    

def add_vertex(graphdict,nodenum):#here add a vertex mean total node nums don't change,but add a new vertex
    operation = {}
    while True:
        start = random.randint(0,int(nodenum)-1)
        end = random.randint(0,int(nodenum)-1)
        if (start,end) not in graphdict.keys():
            weight = random.randint(0,100)
            graphdict.setdefault((start,end),weight)
            operation['key'] = (start,end)
            operation['weight'] = weight
            #print (start,end)
            break
            
    return graphdict,nodenum,operation
    

def delete_vertex(graphdict,nodenum): #delete vertex means total nodenum don't change,but delete on existed vertex
    #delete = graphdict.popitem()m 
    #print(delete)
    operation = {}
    delete_key = graphdict.keys()[random.randint(0,len(graphdict)-1)]
    delete = graphdict.pop(delete_key)
    operation['key']=delete_key
    return graphdict,nodenum,operation  
 #it may exist such a problem: if the deleted node happens to have one vertex,the graph may have a isolated node
         
def modify_weight(graphdict,nodenum):  #select one existed vertex,and modify its weight
    operation = {}
    modify_key = graphdict.keys()[random.randint(0,len(graphdict)-1)]
    operation['key'] = modify_key
    origin_weight = graphdict[modify_key]
    operation['origin_weight'] = origin_weight
    while True:
        modify_weight = random.randint(0,50)
        if modify_weight != origin_weight:
            break
    graphdict[modify_key] = modify_weight
    operation['modify_weight'] = modify_weight
    return graphdict,nodenum,operation

def add_node(graphdict,nodenum):#randomly select an existed node ,add one new node and  add a vertex between these two nodes
    operation={}
    end_node = graphdict.keys()[random.randint(0,len(graphdict)-1)][0]
    weight = random.randint(0,100)
    operation['key'] = (int(nodenum),end_node) 
    operation['weight'] = weight
    graphdict.setdefault((int(nodenum),end_node),weight)
    nodenum_new = int(nodenum)+1
    return graphdict,nodenum_new,operation


def delete_node(graphdict,nodenum):
    operation = {}
    delete_node =  graphdict.keys()[random.randint(0,len(graphdict)-1)][0]   #randomly select one node and delete all the vertexes related with the node 
    #print(delete_node)
    operation['delete_node'] = delete_node
    for key in graphdict.keys():
        if delete_node in key:
            graphdict.pop(key)                 #delete the vertex connected to the node
        elif int(key[0]) > int(delete_node):
            weight = graphdict[key]
            new_start = int(key[0])-1
            if int(key[1]) > int(delete_node):
                new_end = int(key[1])-1   #modify the node num is larger than the original 
            else:
                new_end = int(key[1])
            graphdict.pop(key)
            graphdict.setdefault((new_start,new_end),weight)
        elif int(key[1]) > int(delete_node):
            weight = graphdict[key]
            new_end = int(key[1])-1
            new_start = int(key[0])
            graphdict.pop(key)
            graphdict.setdefault((new_start,new_end),weight)
        else:
            continue
            #print(key)
    nodenum_new = int(nodenum) -1
    return graphdict,nodenum_new,operation
    

def txt_to_dict(filepath):
    graphdict = OrderedDict()
    try:
        with open(filepath) as f:
            nodenum = f.readline().strip('\n')
            while True:
                line = f.readline().strip('\n').split(' ')
                    #print(line)
                if not line:
                    break
                graphdict.setdefault((int(line[0]),int(line[1])),int(line[2]))
        f.close()
    except:
            pass  
    return graphdict,nodenum

def modify(filefolder,modify_round):
    filenum  = len(os.listdir(filefolder))
    destfolder = "modify/"+str(modify_round)
    modifies = []
    #[{'seed_folder':filefolder,'dest_folder':destfolder}]
    jsonpath = "seed_record.json"
    file_id = select_fileid(jsonpath)
    #file_id = random.randint(0,filenum)#random select a file from folder
    filename = str(file_id) + '.txt'
    filepath = os.path.join(filefolder,filename) #read all the files under the folder
    (graphdict,nodenum) = txt_to_dict(filepath) #read txt and turned into a graph
    prob = random.random()
    if prob >=0 and prob<=0.1:
        if int(nodenum) == 1:
                (modified,nodenum_new,operation) = add_node(graphdict,nodenum)
                mode = 4
        else:
                (modified,nodenum_new,operation) = delete_node(graphdict,nodenum) #delete_node 
                mode= 0
                if(len(modified)==0):
                    (modified,nodenum_new,operation) = add_node(graphdict,nodenum) 
                    mode = 4                                 #there are two node with one vertex ,then delete one node ,become null
    elif prob >0.1 and prob <=0.2:
        if int(nodenum) == 1:
                (modified,nodenum_new,operation) = add_vertex(graphdict,nodenum)
                mode = 3
        else:
                (modified,nodenum_new,operation) = delete_vertex(graphdict,nodenum)
                mode = 1
                if(len(modified)==0):
                    (modified,nodenum_new,operation) = add_vertex(graphdict,nodenum) 
                    mode = 3   
    elif prob >0.2 and prob <=0.3:
                (modified,nodenum_new,operation) = modify_weight(graphdict,nodenum)
                mode = 2
    elif prob >0.3 and prob <=0.7:
                (modified,nodenum_new,operation) = add_vertex(graphdict,nodenum)
                mode = 3
    elif prob >0.7 and prob <=1.0:
                (modified,nodenum_new,operation) = add_node(graphdict,nodenum)
                mode = 4
    modified = sorted(modified.items(),key = operator.itemgetter(0))
    modifies.append(Operation(int(file_id),mode,operation))
    new_id  = filenum #start with 0  
    extend_filename = str(new_id)+'.txt'
    filepath = os.path.join(destfolder,extend_filename)
    if not os.path.exists(destfolder):
            os.makedirs(destfolder)
    with open(filepath,'w') as f:           #record new modified file
             f.write(str(nodenum_new)+'\n')
             for line in modified:
                #print(line)
                write_line = str(line[0][0])+' '+str(line[0][1])+' '+str(line[1])+'\n'
                f.write(write_line)
    f.close()
    modify_path = "modify_log"
    if not os.path.exists(modify_path):
            os.makedirs(modify_path)
    recordpath  = os.path.join('modify_log',str(modify_round)+'.json')
    with open(recordpath,'w') as f:
        json.dump(modifies,f,default=lambda o: o.__dict__,indent = 4)
    f.close()
     
'''
coverage
modify_cnt
'''

def load_json(filepath):
    with open (filepath,'r') as f:
        content = json.load(f)
    f.close()
    content.sort(key=lambda x:x["fileid"])
    return content



def select_fileid(jsonpath):
    content = load_json(jsonpath)
    cov_list = [content[i]['cov'] for i in range(len(content))] #recompute the distribution 
    counter = Counter(cov_list).most_common()#OrderedDict(reversed()))
    #print(counter)
    cov_list = []
    rank = []
    for i in range(len(counter)):
        cov_list.append(counter[i][0])
    max_cov = float(max(cov_list))
    rank = [max_cov/(cov_list[i])*(i+1)  for i in range(len(counter))] #cov less priority more ;distribution less priority more
    #print(rank)
    cov_select = cov_list[np.argsort(rank)[-1]]
   # print(cov_select)
    candidate_list = []
    #mod_cnt = []
    for i in range(len(content)):
        if content[i]['cov'] == cov_select:
            candidate_list.append(content[i]['fileid'])
    fileid = candidate_list[random.randint(0,len(candidate_list)-1)]
    if (~os.path.exists("covlist.npy")):
        np.save("covlist.npy",cov_list)    #save cov_list:current
    content[int(fileid)]['mod_cnt'] += 1
    with open(jsonpath,'w') as f:
        json.dump(content,f,default=lambda o: o.__dict__,indent = 4)
    f.close() #for now I haven't considered selecting fileid by mod_cnt
    return fileid
    #print(fileid)



if __name__=="__main__":
    filefolder = "seed"
    modify_round = sys.argv[1]
    modify(filefolder,modify_round)
    #jsonpath = "seed_record.json"
    #select_fileid(jsonpath)
   