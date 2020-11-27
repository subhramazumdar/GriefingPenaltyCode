import os
import sys
txval=10000
path=20
penalty=0.001
budget=1000000
for z in os.listdir(sys.argv[1]):
    txval=50000
    while txval<=110000:
        budget=1000000    
        while budget<=310000000:    
            print(z)
            k="snapshots/"+z
            print(k)
            
            os.system("python3 graph_channel_collateral.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(budget)+" output_collateral.csv")
            budget=budget*2
            
        txval=txval+20000

