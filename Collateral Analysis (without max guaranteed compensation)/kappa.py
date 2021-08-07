import os
import sys
txval=5000
path=5


for z in os.listdir(sys.argv[1]):
    
    
        kappa=1
        while kappa<=4:
            budget=5000000
            while budget<=700000000:
                penalty=0.00012*kappa
                txval=10000
                while txval<=10000:
                    path=5
                    while path<=20:
                        print(z)
                        k="snapshots/"+z
                        print(k)            
                        os.system("python3 graph_collateral_flowconstant.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(budget)+" "+str(2016/path)+" "+"output-extra-collateral"+str(kappa)+".csv")
               
                        path=path+5
                    txval=txval*2
            
                budget=budget*5
            kappa=kappa+1
        
