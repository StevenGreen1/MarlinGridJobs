#!/bin/bash

for i in {61..68}
do
    python MakeConfigFile.py /r06/lc/sg568/ReviewJER/CalibrationResults/Stage${i}/5x5_30x30/ILD_o1_v06_AAxAA_BBxBB_XX_YY.xml Stage${i}Config_5x5_30x30.py
done
