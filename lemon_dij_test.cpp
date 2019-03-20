#include <iostream>
#include <vector>
#include <map>
#include <fstream>
#include <string>
#include <cassert> 
#include <lemon/smart_graph.h>
#include <lemon/dijkstra.h>

using namespace std;
using namespace lemon;

struct Arc
{
   string sourceID;
   string targetID;
   int cost;
};




int main(int argc,char *argv[])
{
  SmartDigraph g;
  SmartDigraph::ArcMap<int> costMap(g);
  SmartDigraph::NodeMap<string> nodeMap(g);
  //read input file
  ifstream infile;
  string inputfile=argv[1];//,outputfile= argv[2];

  infile.open(inputfile.data());

  assert(infile.is_open());
  string s;
  getline(infile,s);//get first line-nodenum
  int node_num = atoi(s.c_str());
  
  //init nodes
  vector<pair<string,int>> nodes;
  for (int i=0;i<node_num;++i){
       nodes.push_back(make_pair(to_string(i),i));
  }
  //int count =0;
  vector<Arc> arcs;
  string start,end,weight;
  //cout <<"hello"<<endl;
  while(infile>>start>>end>>weight){
      //cout <<count<<endl;
      //count +=1;
      arcs.push_back(Arc{start,end,atoi(weight.c_str())});//read input files(start-point,end-point,weight)
  }
 

  //define the type of the dijkstra class
  using SptSolver = Dijkstra<SmartDigraph, SmartDigraph::ArcMap<int>>;
  //populate graph;
  SmartDigraph::Node currentNode;  
  for(auto nodeIter=nodes.begin();nodeIter!=nodes.end();++nodeIter){
      string key = nodeIter->first;
      currentNode = g.addNode();
      nodeMap[currentNode] = key;
  }

  //arcs with the costs through the cost map
  SmartDigraph::Arc currentArc;
  for(auto arcsIter = arcs.begin();arcsIter != arcs.end();++arcsIter){
      SmartDigraph::Node sourceNode = g.nodeFromId(atoi(arcsIter->sourceID.c_str()));
      SmartDigraph::Node targetNode = g.nodeFromId(atoi(arcsIter->targetID.c_str()));
      currentArc = g.addArc(sourceNode,targetNode);
      costMap[currentArc] = arcsIter->cost;
  }

  //add source and target  
  string end_node = to_string(node_num -1);
  //string out_filename; 
  //out_filename ="result/"+index+".txt";
  //ofstream out(outputfile);
  //out <<"0"<<" "<<end_node<<endl;
  //cout <<"0"<<" "<<end_node<<endl;

try{
  SmartDigraph::Node startN = g.nodeFromId(0);
  SmartDigraph::Node endN = g.nodeFromId(node_num-1);
  SptSolver spt(g,costMap);
  spt.run(startN,endN);
  bool reachable= true;//judge whether we have a path;
  vector< SmartDigraph::Node> path;
  for (SmartDigraph::Node v= endN;v!=startN;v=spt.predNode(v)){
      if(g.id(v)<0) {
          reachable = false;// node-id must be >0
          break;
      }
      if(v!= lemon::INVALID && spt.reached(v))
      {
          path.push_back(v);
          
      }
  }
  int cost = spt.dist(endN);
  if (path.empty()) reachable = false;
  path.push_back(startN);
  
  if(reachable == true){
  for(auto p= path.rbegin();p!=path.rend();++p)
      {cout <<nodeMap[*p]<<' ';
      }
  //out<<endl;
      //cout <<p<<endl;
  }
  cout <<"Total cost for the shortest path is: "<<cost<<endl;
  //out <<cost<<endl;
  //out<<endl;
  //out.close();
}catch(...){


}
 
return 0;
}
