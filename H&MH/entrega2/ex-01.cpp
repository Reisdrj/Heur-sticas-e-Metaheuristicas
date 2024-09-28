#include <bits/stdc++.h>
using namespace std;

string toBinary(int n)
{
    string r;
    while(n!=0) {r=(n%2==0 ?"0":"1")+r; n/=2;}
    return r;
}

int main(){
    srand(time(NULL));
    clock_t t;

    int tam;
    cin >> tam;
    long long bin_size = pow(2, tam);

    t = clock();
    for(int i = 0; i < bin_size; i++){
        string result = toBinary(i);
        result.insert(0, tam - result.length(), '0');
        cout << result << endl;
    }
    t = clock() - t;
    cout << "Tempo de processamento (em segundos): " << ((float)t)/CLOCKS_PER_SEC << endl;
    return 0;
}