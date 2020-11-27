import os
import sys
txval=10000
budget=3000000

for z in os.listdir(sys.argv[1]):
      penalty=0.00000001
      while penalty<=0.1:    
            print(z)
            k="snapshots/"+z
            print(k)
            s="output_synthetic_test.csv"
            os.system("python3 graph_main_attack.py "+str(k)+" "+str(budget)+" "+str(penalty)+" "+str(txval)+" output_gamma.csv")
            penalty=penalty*10
            
        

