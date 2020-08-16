#!/bin/bash 

# Setting the griefing penalty rate as 0.0001
penalty=0.001

###################################################
##  Script to mount attack by creating channels  ##
###################################################

# Iterating over txn sizes (in satoshi)
for((txval=1;txval<=100000;txval=txval*10))
do
    # Iterating over budget of the attacker (in satoshi)
    for((budget=3000;budget<=300000000;budget=budget*10))
    do
        # For every snapshot, mount the attack and write to output file
        for snapshot in snapshots/*.json
        do
            python3 graph_main_attack.py $snapshot $budget $penalty $txval output_synthetic.csv
        done
    done
done


########################################################
##  Script to mount attack without creating channels  ##
########################################################

# Iterating over txn sizes (in satoshi)
for((txval=1;txval<=100000;txval=txval*10))
do
    # Iterating over budget of the attacker (in satoshi)
    for((budget=3000;budget<=3000000;budget=budget*10))
    do
        # For every snapshot, mount the attack and write to output file
        for snapshot in snapshots/*.json
        do
            python3 graph_main_no_change_attack.py $snapshot $budget $penalty $txval output_original.csv
        done
    done       
done
