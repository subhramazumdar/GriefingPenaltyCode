import os
import sys
txval=5000
path=5


for z in os.listdir(sys.argv[1]):
    
    
        divide=1
        zeta=0.05
        kappa=1
        while zeta<=0.5:
            penalty=0.000036
            while penalty<=0.000048:
                budget=5000000
                while budget<=700000000:
                    
                    txval=20000
                    while txval<=20000:
                        path=20
                        
                        print(z)
                        k="snapshots/"+z
                        print(k)            
                        os.system("python3 graph_collateral_flowconstant.py "+str(k)+" "+str(penalty)+" "+str(divide)+" "+str(zeta)+" "+str(txval)+" "+str(path)+" "+str(budget)+" "+str(2016/path)+" "+"output-zeta1.csv")
                        txval=txval*2
            
                    budget=budget*5
                penalty=penalty+0.000012
            zeta=zeta+0.05
