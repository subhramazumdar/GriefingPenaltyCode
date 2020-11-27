import os
import sys
txval=50000
path=5
penalty=0.001
for z in os.listdir(sys.argv[1]):
    
    path=5
    while path<=20:
        penalty=0.00000001     
        while penalty<=0.1:    
            print(z)
            k="snapshots/"+z
            print(k)
            
            os.system("python3 graph_channel.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" output_channel_gamma.csv")
            penalty=penalty*10
            
        path=path+5

