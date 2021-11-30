import os
import sys
txval=5000
path=5
corrupt=0
transact=3000
for z in os.listdir(sys.argv[1]):
        
        penalty=0.000001
        while penalty<=0.000001:
            print(z)
            k="snapshots/"+z
            print(k)
            path=5
            while path<=20:
                txval=5000
                while txval<=80000:
                 
                
                    transact=3000 
                    while transact<=9000:
                        os.system("python3 test_new.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(penalty)+" "+str(transact)+" "+str(path)+" output_test"+str(penalty)+".csv")
                        transact=transact+2000
                
                    txval=txval*2
                path=path+5        
                
            penalty=penalty*10
        

