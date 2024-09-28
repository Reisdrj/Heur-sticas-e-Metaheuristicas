#include <bits/stdc++.h>
using namespace std;

long int measureNodesDistance(int node1, int node2,
                              vector<vector<long int>> &positions) {
  long int xd = positions[node1][1] - positions[node2][1];
  long int yd = positions[node1][2] - positions[node2][2];
  return (long int)round(sqrt(xd * xd + yd * yd) + 0.5);
}

int main() {

  int qntd;
  cin >> qntd;
  vector<vector<long int>> positions(qntd, vector<long int>(3));
  vector<vector<long int>> AdjMatrix(qntd, vector<long int>(qntd));
  vector<int> nodes(qntd);
  iota(nodes.begin(), nodes.end(), 1);
  vector<long int> solution(qntd);
  solution[0] = 0;
  vector<long int> visited(qntd, 0);
  visited[0] = 1;
  
  // Input
  for (int i = 0; i < qntd; i++) {
    cin >> positions[i][0] >> positions[i][1] >> positions[i][2];
  }

  // Calculate Adjacency Matrix
  for (int i = 0; i < qntd; i++) {
    for (int j = 0; j < qntd; j++) {
      if (i == j) {
        AdjMatrix[i][j] = INT_MIN;
        continue;
      }
      AdjMatrix[i][j] = measureNodesDistance(i, j, positions);
    }
  }

  for (int i = 0; i < qntd; i++) {
    for (int j = 0; j < qntd; j++) {
      cout << AdjMatrix[i][j] << " ";
    }
    cout << endl;
  }

  cout << endl; 

  int line = 0;

  for(int i = 1; i < qntd; i++){
    int value = INT_MIN, index = 0;
    for(int j = 0; j < qntd; j++){
      if(AdjMatrix[line][j] > value && visited[j] == 0){
        value = AdjMatrix[line][j];
        index = j;
        //cout << endl << value << " ----> " << index << endl;
      }
    }
    visited[index] = 1;
    solution[i] = index;
    line = index;
    //cout << value << " ---> " << index << endl;
  }

  // Solve problem by the most closure city
  /*for (int i = 0; i < qntd; i++) {
    vector<int> indexes(qntd);
    iota(indexes.begin(), indexes.end(), 0);


  }*/
  
  // Output
  cout << "Solução: ";
  for(int i = 0; i < qntd; i++){
    cout << solution[i] << " ";
  }
  cout << endl;

  return 0;
}