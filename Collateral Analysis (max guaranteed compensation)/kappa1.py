import os
import sys
txval=5000
path=5


for z in os.listdir(sys.argv[1]):
    
    kappa=1
    zeta=0.05
    while zeta<=0.15:
        while kappa<=1:
            budget=5000000
            while budget<=700000000:
                penalty=0.05*((zeta*zeta)/(2*zeta+kappa-zeta))
                txval=10000
                while txval<=10000:
                    path=2
                    while path<=int(kappa/zeta):
                        print(z)
                        k="snapshots/"+z
                        print(k)            
                        os.system("python3 graph_collateral_flowconstant.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(budget)+" "+str(2016/path)+" "+"outputcollateral"+str(kappa)+".csv")
               
                        path=path+1
                    txval=txval*2
            
                budget=budget*5            
        zeta=zeta+0.05
