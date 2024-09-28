#include <bits/stdc++.h>
using namespace std;

const int ITERATIONS = 100;

bool verification(const vector<int> &solution, const vector<pair<int,int>> &elementos, const int &pesoMax, int &profit){
    int weight = 0;
    int actualProfit = 0;

    for(int i = 0; i < solution.size(); i++){
        if(solution[i] == 1){
            weight += elementos[i].second;
            actualProfit += elementos[i].first;
        }
    }

    if(weight < pesoMax){
        profit = actualProfit;
        return true;
    }
    else{
        return false;
    }
}

void bestImprovmemt(vector<int> &solution, const int &pesoMax, const vector<pair<int,int>> &elementos, int &profitT){
    vector<int> candidato = solution;
    int bestProfit = 0;
    int proportion = 0;
    int pos = 0;
    int profit = 0;
    for(int i = 0; i < solution.size(); i++){
        candidato = solution;
        if(candidato[i] == 0){
            candidato[i] = 1;
        }
        if(verification(candidato, elementos, pesoMax, profit) && profit > bestProfit){
            bestProfit = profit;
            pos = i;
        }
    }
    profitT = bestProfit;
    solution[pos] = 1;
}


void BuscaLocal(vector<int> &solution, const int &pesoMax, const vector<pair<int,int>> &elementos, int &value){
    int profit = 0;
    vector<int> candidato(solution.size());
    vector<int> aux(solution.size());
    int bestProfit = 0;
    int proportion = 0;
    int peso = 0;
    int cond = 0;

    for(int i =0; i < ITERATIONS; i++){
        bestImprovmemt(solution, pesoMax, elementos, bestProfit);
    }
    value = bestProfit;
}

int main(){
    int qntd, peso; cin >> qntd >> peso;
    vector<pair<int,int>> elementos(qntd, pair<int,int>());
    vector<int> binaria(qntd, 0);
    int profitTotal = 0;

    for(int i = 0; i < qntd; i++){
        cin >> elementos[i].first >> elementos[i].second;
    }

    BuscaLocal(binaria, peso, elementos, profitTotal);

    cout << endl;
    for(int i = 0; i < binaria.size(); i++){
        cout << binaria[i] << ' ';
    }
    cout << " ------> " << profitTotal << endl << endl;

    return 0;
}