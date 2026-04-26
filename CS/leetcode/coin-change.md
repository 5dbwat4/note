```c
        int lalm[10008];

        int min(int a,int b){return a>b?b:a;}
int coinChange(int* coins, int coinsSize, int amount) {
        if(amount==0)return 0;
        for(int i=1;i<=amount;i++){
            int currmin=0x77ffff;
            for(int oo=0;oo<coinsSize;oo++){
                if(i<coins[oo]){
                    continue;
                }
                if(i==coins[oo]){
                    currmin=0;break;
                }

                if(lalm[i-coins[oo]]!=0){
                    currmin=min(lalm[i-coins[oo]],currmin);
                }

                
            }
            if (currmin==0x77ffff)lalm[i]=0;
            else lalm[i]=currmin+1;
        }
        if(lalm[amount]==0)return -1;
        return lalm[amount];
}
```