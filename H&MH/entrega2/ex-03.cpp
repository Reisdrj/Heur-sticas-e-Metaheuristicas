#include <bits/stdc++.h>
using namespace std;

int main(){
    srand(time(NULL));
    clock_t t;

    int nodesNum, edgesNum;
    cin >> nodesNum >> edgesNum;
    vector<int> nodes(nodesNum);
    iota(nodes.begin(), nodes.end(), 1);
    vector<vector<int>> edges(nodesNum+1, vector<int>(nodesNum+1, INT_MAX));
    t = clock();
    for(int i = 0; i < edgesNum; i++){
        int e1, e2, c;
        cin >> e1 >> e2 >> c;
        edges[e1][e2] = c;
        edges[e2][e1] = c;
    }
    int count = 0;
    cout << endl << "     Paths       " << "    Costs  " << endl;
    do{
        bool valid = true;
        int cost = 0;
        for(int i = 1; i < nodesNum; i++){
            if(edges[nodes[i-1]][nodes[i]] == INT_MAX || edges[nodes[5]][nodes[0]] == INT_MAX){
                //cout << "===" << nodes[i] << " ---- " << nodes[i+1] << endl;
                valid = false;
            }
            //cout << "===" << nodes[i-1] << " ---- " << nodes[i] << " - = - " << valid << endl;
            if(valid){
                    cost += edges[nodes[i-1]][nodes[i]];
            }
        }
        cost += edges[nodes[5]][nodes[0]];
        if(valid){
            count++;
            for(int i : nodes){
                    cout << i << ' ';
                }
            //cout << "-=-=" << nodes[nodesNum-1] << endl;
            cout << nodes[0];
            cout << " -------- " << cost << endl;
        }
    }while(next_permutation(nodes.begin(), nodes.end()));
    t = clock() - t;
    cout << endl << "Number of valid paths: " << count << endl;
    cout << "Tempo de processamento: " << ((float)t)/CLOCKS_PER_SEC << endl;
    return 0;
}