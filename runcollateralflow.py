import os
import sys
txval=5000
path=20


for z in os.listdir(sys.argv[1]):
    budget=1000000
    while budget<=310000000:
        penalty=0.00000001
        while penalty<=0.1:    
            print(z)
            k="snapshots/"+z
            print(k)
            
            os.system("python3 graph_collateral_flowconstant.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(budget)+" output_collateral_flow_new.csv")
            penalty=penalty*10
            
        budget=budget*2

