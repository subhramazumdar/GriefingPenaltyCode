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
        path=20
        while path<=20:
            profit=3
        
            while profit<=3:
                txval=15000
                while txval<=60000:
                    corrupt=0.02
                    while corrupt<30:
                        transact=20000
                        while transact<=20000:
                            frac=1000
                            while frac<=1000:
                                q=0.7
                                while q<=0.7:
                                    print(corrupt)
                                    os.system("python3 gametheory.py "+str(k)+" "+str(penalty)+" "+str(txval)+" "+str(path)+" "+str(profit)+" "+str(corrupt)+" "+str(transact)+" output_gt_jisa.csv"+" "+str(frac)+" "+str(q))
                                    q=q+0.2
                                frac=frac*10
                            break
                        corrupt=corrupt*2
                    txval=txval*2
                profit=profit+4
            path=path+5
            
