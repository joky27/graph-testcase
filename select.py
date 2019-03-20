import sys
import os
import pandas as pd 
import numpy as np 
import json 
import shutil
import re
#next iteration seed file select
#select rule 1:coverage up
#step 1:select file_id need to remove
#step 2:at the same time change the coverage folder and cov_grep (temp)
#step 3:record operation in select_log folder

def load_json(filepath,filetype):
    with open (filepath,'r') as f:
        content = json.load(f)
    f.close()
    if filetype == 'modify':
        content = content[1:]
    content.sort(key=lambda x:x["fileid"])
    return content

def load_path(filepath):
    with open(filepath,'r') as f:
        content = f.readlines()
    f.close()
    if(len(content)==4):
        path = content[1].strip('\n').split(' ')[:-1]   #strip the \n at the end,and split by space.#-1 means the space at the end
    else:
        path =[]
    return path 

def load_coverage(filepath):
    with open(filepath) as f:
        file_context = f.read() #read the context
        coverage_pattern = re.compile('<td class="headerCovTableEntry">(.*?)</td>',re.S)
        items = re.findall(coverage_pattern,file_context) #coverage_info
        line_coverage = int(items[0])
    f.close()
    return line_coverage

    
#accept:combine_cov >seed_cov || single_cov don't belong to the covlist ||belong to the little ones
def coverage_compare(index):     
    combine_path = "cov/combine.txt"
    seed_path ='seed.txt'
    combine_cov = load_coverage(combine_path)
    seed_cov = load_coverage(seed_path)
    
    #os.remove(combine_path)
    if combine_cov > seed_cov:
        os.remove("cov/seed.txt") 
        os.rename("cov/combine.txt","cov/seed.txt")
        os.remove("info/seed.info") 
        filename = "info/"+str(index)+'.info'
        os.rename(filename,"info/seed.info")
        source_path = "modify/"+str(index)
        filename = os.listdir(source_path)[0]
        shutil.copy(os.path.join(source_path,filename),os.path.join("seed",filename))
    else:
        os.remove("cov/combine.txt") 

   
    

if __name__ == "__main__":
    index = sys.argv[1]
    coverage_compare(index)
    #cov_dict = coverage_compare(last_index,new_index)   
    


        
        
