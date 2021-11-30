import os
import sys
txval=5000
path=5


for z in os.listdir(sys.argv[1]):
    
    
        divide=1.5
        zeta=0.075
        kappa=1
        while zeta<=0.75:
            kappa=1
            while kappa<=1:
                budget=5000000
                while budget<=700000000:
                    
                    txval=20000
                    while txval<=20000:
                        path=int(divide/zeta)
                        penalty=divide/(10*10*(200+1900))
                        print(z)
                        k="snapshots/"+z
                        print(k)            
                        os.system("python3 graph_collateral_flowconstant.py "+str(k)+" "+str(penalty)+" "+str(divide)+" "+str(zeta)+" "+str(txval)+" "+str(path)+" "+str(budget)+" "+str(2016/path)+" "+"output-zeta1.5.csv")
                        txval=txval*2
            
                    budget=budget*5
                kappa=kappa+1
            zeta=zeta+0.05
