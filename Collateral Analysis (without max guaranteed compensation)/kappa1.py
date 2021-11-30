import os
import sys
txval=5000
path=5


for z in os.listdir(sys.argv[1]):
    
    
        kappa=1
        penalty=0.0000001
        while penalty<=0.0000001:
            while kappa<=1:
                budget=5000000
                while budget<=700000000:
                    
                    txval=10000
                    while txval<=100000:
                        path=20
                        while path<=20:
                            print(z)
                            k="snapshots/"+z
                            print(k)            
                            os.system("python3 graph_collateral_flowconstan-lowt.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(budget)+" "+str(2016/path)+" "+"output-extra-collateral-less0.0000001.csv")
                
                            path=path+5
                        txval=txval*2
            
                    budget=budget*5
                kappa=kappa+1
            penalty=penalty*10
