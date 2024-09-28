#include <bits/stdc++.h>
using namespace std;

int main(){
    int qntd, peso; cin >> qntd >> peso;
    vector<vector<float>> elementos(qntd, vector<float>(3, 0));
    vector<int> binaria(qntd, 0);
    int partialWeight = 0;
    int cont = 0;
    int profit = 0; 

    for(int i = 0; i < qntd; i++){
        cin >> elementos[i][0] >> elementos[i][1];
        elementos[i][2] = elementos[i][1] / elementos[i][0];
    }

    for(int i = 0; i < qntd; i++){
        cout << elementos[i][0] << " " << elementos[i][1] << " " << elementos[i][2] << endl;
    }


    cout << " -------- " << endl;

    sort(elementos.begin(), elementos.end(), [](const vector<float>& a, const vector<float>& b) {
            return a[1] < b[1];
    });

    for(int i = 0; i < qntd; i++){
        if((partialWeight + elementos[i][1]) < peso){
            partialWeight += elementos[i][1];
            profit += elementos[i][0];
            binaria[i] = 1;
        }
    }

    for(int i = 0; i < qntd; i++){
        cout << binaria[i] << " ";
    }

    cout << "-----> " << partialWeight << " :: " << profit << endl;

    return 0;
}