import os
import sys
txval=20000
path=4
penalty=0.001
for z in os.listdir(sys.argv[1]):
    txval=20000
    while txval<=100000:
        path=5
        while path<=20:
            penalty=1.00E-05
            while penalty<=0.0013:    
                print(z)
                k="snapshots/"+z
                print(penalty)
            
                os.system("python3 ratiointersect.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" output_ratio_select.csv")
                penalty=penalty*2
        
            path=path+5
        txval=txval+20000

