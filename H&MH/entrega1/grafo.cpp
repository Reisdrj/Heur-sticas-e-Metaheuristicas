#include <bits/stdc++.h>
using namespace std;

int main(){
    int v, a;
    cin >> v >> a;
    vector <vector<int>> matrix (v+1, vector<int> (v+1, 0));
    vector <list<pair<int, int>>> lista (v+1);
    cout << "//// Matriz de Adjacência ////" << endl;
    for (int i = 0; i < a; i++){
        int v1, v2, p;
        cin >> v1 >> v2 >> p;
        matrix[v1][v2] = matrix[v2][v1] = p;
        lista[v1].emplace_back(v2, p);
        lista[v2].emplace_back(v1, p);
    }
    for (int i = 1; i <= v; i++){
        for(int j = 1; j <= v; j++){
            cout << matrix[i][j] << ' ';
        }
        cout << endl;
    }
    cout << "//// Lista de Adjacência ////" << endl;
    for (int i = 1; i <= v; i++){
        cout << i << " -> ";
        for (auto p : lista[i]){
            cout << '(' << p.first << ", " <<p.second << ')' << ' ';
        }
        cout << endl;
    }
}