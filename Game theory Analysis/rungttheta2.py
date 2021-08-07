import os
import sys
txval=1000
path=2
corrupt=5
transact=13000
for z in os.listdir(sys.argv[1]):
        penalty=0
        
        print(z)
        k="snapshots/"+z
        print(k)
        path=5
        while path<=20:
            profit=0.00001
        
            while profit<=0.0005:
                txval=15000
                while txval<=60000:
                    corrupt=0
                    while corrupt<90:
                        transact=20000
                        while transact<=20000:
                            print(corrupt)
                            os.system("python3 gametheorytheta2.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(profit)+" "+str(corrupt)+" "+str(transact)+" output_gt_newtheta2.csv")
                            break
                        corrupt=corrupt+10
                    txval=txval*2
                profit=profit*5
            path=path+5
            
