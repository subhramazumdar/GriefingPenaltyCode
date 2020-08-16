
penalty=0.001

for((txval=1;txval<=100000;txval=txval*10))
do
   for((budget=3000;budget<=300000000;budget=budget*10))
    do
        
        
            for z in snapshots/*.json
            do
                python3 graph_main_attack.py $z $budget $penalty $txval output_synthetic.csv
            done
        
    done
done
for((txval=1;txval<=100000;txval=txval*10))
do

   for((budget=3000;budget<=3000000;budget=budget*10))
      do
        
        
            for z in snapshots/*01.json
            do
                python3 graph_main_no_change_attack.py $z $budget $penalty $txval output_original.csv
            done
      done       
done
