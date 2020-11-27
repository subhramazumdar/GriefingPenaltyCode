import os
import sys
txval=50000
path=4
penalty=0.001
for z in os.listdir(sys.argv[1]):
    
    txval=50000
    while txval<=110000:
        path=4
        while path<=20:    
            print(z)
            k="snapshots/"+z
            print(k)
            
            os.system("python3 graph_channel.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" output_channel.csv")
            path=path+2
        
        txval=txval+20000    
        

