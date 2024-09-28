#include <bits/stdc++.h>
using namespace std;

void permutations(string num, int ini, int final){
    if(ini == final){
        cout << num << endl;
    }
    else{
        for(int i = ini; i <= final; i++){
            swap(num[ini], num[i]);

            permutations(num, ini + 1, final);

            swap(num[ini], num[i]);
        }
    }
}

int main(){
    srand(time(NULL));
    clock_t t;

    int tam; cin >> tam;
    string num;
    cout << endl << "Permutations" << endl;
    for(int i = 1; i <= tam; i++){
        num = num + to_string(i);
    }
    t = clock();
    permutations(num, 0, num.length()-1);
    t = clock() - t;
    cout << endl << "Tempo de processamento: " << ((float)t)/CLOCKS_PER_SEC << endl;
    return 0;
}