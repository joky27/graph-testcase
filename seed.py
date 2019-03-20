from random import randint,shuffle
import datetime
import sys
import os
import select
import re
import json
#from select import load_coverage
#weighted direct graph(may include circle)

#used to generate seed testcase
#folder:the destation folder that you need to generate seed samples
class Operation:
    def __init__(self,fileid,coverage,mod_cnt):
        self.fileid = fileid
        self.cov = coverage
        self.mod_cnt = mod_cnt 
    
    def __repr__(self):
        return repr((self.fileid,self.cov,self.mod_cnt))

def generate_seed(folder):
     starttime = datetime.datetime.now()
     print("start generate seed samples")
     for i in range(1000): #100 random seed
         node_num = randint(100,1000) 
         nodes = range(node_num)
         edges = []
         for x in nodes:
             for y in nodes:
                 edges.append((x,y)) 
         shuffle(edges)
         edge_num =  randint(2000,4000)    
         edges_list = sorted(edges[0:edge_num+1:1])
         content = []
         content.append(str(node_num))
         for j in range(edge_num+1):
              weight = randint(1,10) #weight from 0-10
              write_content ='\n'+str(edges_list[j][0])+' '+str(edges_list[j][1])+' '+str(weight)
              content.append(write_content)
         content.append('\n')
         filename = str(i)+'.txt'
         filepath=os.path.join(folder,filename)
         with open(filepath,'a') as f:
              f.writelines(content)
     f.close()
     endtime = datetime.datetime.now()
     print("generate seed finished")
     duration =(endtime-starttime).seconds
     print("total duration is"+str(duration)+"s")

def load_coverage(filepath):
    with open(filepath) as f:
        file_context = f.read() #read the context
        coverage_pattern = re.compile('<td class="headerCovTableEntry">(.*?)</td>',re.S)
        items = re.findall(coverage_pattern,file_context) #coverage_info
        line_coverage = int(items[0])
    f.close()
    return line_coverage

def get_seed_cov(filepath):#read cov info from cov folder
     filelist = os.listdir(filepath)
     seed_cov = []
     for filename in filelist:
           print(filename)
           fileid = filename.split('.')[0]
           filepath = os.path.join("cov",filename)
           filecov = int(load_coverage(filepath))
           mod_cnt = 0
           seed_cov.append(Operation(int(fileid),filecov,mod_cnt))
     with open("seed_record.json",'w') as f:
           json.dump(seed_cov,f,default=lambda o: o.__dict__,indent = 4)
     f.close()



if __name__=='__main__':
     foldername = sys.argv[1]
     num = sys.argv[2]
     #filefolder = os.path.join(foldername,'0')
     if num == "1":
          os.makedirs(foldername)
          generate_seed(foldername)
     else:
          filepath = "seed"
          get_seed_cov(filepath)    
