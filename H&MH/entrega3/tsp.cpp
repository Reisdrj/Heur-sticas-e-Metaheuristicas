#include<bits/stdc++.h>
using namespace std;
typedef std::vector<int> nodes;
#define ITERATIONS 2000

long int measureNodesDistance(int node1, int node2, vector<vector<int>> &positions){
    long int xd = positions[node1][1] - positions[node2][1];
    long int yd = positions[node1][2] - positions[node2][2];
    return (long int) round(sqrt( xd*xd + yd*yd) + 0.5);
}

long int measurePathDistance(nodes &actualPath, vector<vector<int>> &positions){
    long int actualDistance = 0;
    for(int i = 0; i < actualPath.size(); i++){
        actualDistance += measureNodesDistance(actualPath[i] -1, actualPath[(i+1) % actualPath.size()] -1, positions);
    }
    return actualDistance;
}

void twoOpt(nodes &path){
    int pos1 = rand() % path.size();
    int pos2 = rand() % path.size();
    cout << "Pos1: " << pos1 << "  Pos2:" << pos2 << endl;
    swap(path[pos1], path[pos2]);
}

int main(){
    int qntd; cin >> qntd;
    long int bestDistance = INT_MAX;
    long int actualDistance = 0;
    long int test;
    vector<vector<int>> positions(qntd, vector<int> (3));
    nodes nodes(qntd);
    vector<int> bestPath = nodes;
    iota(nodes.begin(), nodes.end(), 1);

    int lowerDistance;

    for(int i = 0; i < qntd; i++){
        cin >> positions[i][0] >> positions[i][1] >> positions[i][2];
    }
    for(int i = 0; i < ITERATIONS; i++){
        twoOpt(nodes);
        actualDistance = measurePathDistance(nodes, positions);
        if(actualDistance < bestDistance){
            bestDistance = actualDistance;
            bestPath = nodes;
        }
    }
    
    cout << "Path: ";
    for(int j = 0; j < qntd; j++){
                cout << bestPath[j] << " ";
    }
    cout << " -----> " << bestDistance << endl;
}