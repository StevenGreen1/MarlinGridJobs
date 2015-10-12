import re
import sys

inputSteeringFile = sys.argv[1]

CalibrECAL = '-1'
CalibrHCAL = '-1'
CalibrHCALBarrel = '-1'
CalibrHCALEndcap = '-1'
CalibrHCALOther = '-1'
CalibrMUON = '-1'
HCALBarrelTimeWindowMax = '-1'
ECALBarrelTimeWindowMax = '-1'
HCALEndcapTimeWindowMax = '-1'
ECALEndcapTimeWindowMax = '-1'
CalibECALMIP = '-1'
CalibHCALMIP = '-1'
ECalToMipCalibration = '-1'
HCalToMipCalibration = '-1'
MuonToMipCalibration = '-1'
ECalMipThreshold = '-1'
HCalMipThreshold = '-1'
ECalToEMGeVCalibration = '-1'
HCalToEMGeVCalibration = '-1'
ECalToHadGeVCalibrationBarrel = '-1'
ECalToHadGeVCalibrationEndCap = '-1'
HCalToHadGeVCalibration = '-1'
MaxHCalHitHadronicEnergy = '-1'

with open(inputSteeringFile) as openFile:
    for line in openFile:
        if 'CalibrECAL' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibrECAL = matchObj.group(2).strip()
        if 'CalibrHCAL' in line and 'CalibrHCALBarrel' not in line and 'CalibrHCALEndcap' not in line and 'CalibrHCALOther' not in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibrHCAL = matchObj.group(2).strip()
        elif 'CalibrHCALBarrel' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibrHCALBarrel = matchObj.group(2).strip()
        elif 'CalibrHCALEndcap' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibrHCALEndcap = matchObj.group(2).strip()
        elif 'CalibrHCALOther' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibrHCALOther = matchObj.group(2).strip()
        elif 'CalibrMUON' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibrMUON = matchObj.group(2).strip()
        elif 'HCALBarrelTimeWindowMax' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                HCALBarrelTimeWindowMax = matchObj.group(2).strip()
        elif 'ECALBarrelTimeWindowMax' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECALBarrelTimeWindowMax = matchObj.group(2).strip()
        elif 'HCALEndcapTimeWindowMax' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                HCALEndcapTimeWindowMax = matchObj.group(2).strip()
        elif 'ECALEndcapTimeWindowMax' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECALEndcapTimeWindowMax = matchObj.group(2).strip()
        elif 'CalibECALMIP' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibECALMIP = matchObj.group(2).strip()
        elif 'CalibHCALMIP' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                CalibHCALMIP = matchObj.group(2).strip()
        elif 'ECalToMipCalibration' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECalToMipCalibration = matchObj.group(2).strip()
        elif 'HCalToMipCalibration' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                HCalToMipCalibration = matchObj.group(2).strip()
        elif 'MuonToMipCalibration' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                MuonToMipCalibration = matchObj.group(2).strip()
        elif 'ECalMipThreshold' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECalMipThreshold = matchObj.group(2).strip()
        elif 'HCalMipThreshold' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                HCalMipThreshold = matchObj.group(2).strip()
        elif 'ECalToEMGeVCalibration' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECalToEMGeVCalibration = matchObj.group(2).strip()
        elif 'HCalToEMGeVCalibration' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                HCalToEMGeVCalibration = matchObj.group(2).strip()
        elif 'ECalToHadGeVCalibrationBarrel' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECalToHadGeVCalibrationBarrel = matchObj.group(2).strip()
        elif 'ECalToHadGeVCalibrationEndCap' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                ECalToHadGeVCalibrationEndCap = matchObj.group(2).strip()
        elif 'HCalToHadGeVCalibration' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                HCalToHadGeVCalibration = matchObj.group(2).strip()
        elif 'MaxHCalHitHadronicEnergy' in line:
            matchObj = re.match('(.*?)>(.*?)</parameter>(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                MaxHCalHitHadronicEnergy = matchObj.group(2).strip()

CalibrECALToPrint = CalibrECAL.split()

configFileString = '# Calibration config file for testing\n' 
configFileString += '# Digitisation Constants - ECal \n'
configFileString += 'CalibrECal = ' + CalibrECALToPrint[0] + '\n'
configFileString += '\n'

configFileString += '# Digitisation Constants ILDCaloDigi - HCal\n'
configFileString += 'CalibrHCalBarrel = ' + CalibrHCALBarrel + '\n'
configFileString += 'CalibrHCalEndcap = ' + CalibrHCALEndcap + '\n'
configFileString += 'CalibrHCalOther = ' + CalibrHCALOther + '\n'
configFileString += '\n'

configFileString += '# Digitisation Constants NewLDCCaloDigi - HCal\n'
configFileString += 'CalibrHCal = ' + CalibrHCAL + '\n'
configFileString += '\n'

configFileString += '# Digitisation Constants - Muon Chamber\n'
configFileString += 'CalibrMuon = ' + CalibrMUON + '\n'
configFileString += '\n'

configFileString += '# MIP Peak position in directed corrected SimCaloHit energy distributions\n'
configFileString += '# used for realistic ECal and HCal digitisation options\n'
configFileString += 'CalibrECalMIP = ' + CalibECALMIP + '\n'
configFileString += 'CalibrHCalMIP = ' + CalibHCALMIP + '\n'
configFileString += '\n'

configFileString += '# MIP Peak position in directed corrected CaloHit energy distributions\n'
configFileString += '# used for MIP definition in PandoraPFA\n'
configFileString += 'ECalToMIPCalibration = ' + ECalToMipCalibration + '\n'
configFileString += 'HCalToMIPCalibration = ' + HCalToMipCalibration + '\n'
configFileString += 'MuonToMIPCalibration = ' + MuonToMipCalibration + '\n'
configFileString += '\n'

configFileString += '# EM and Had Scale Settings\n'
configFileString += 'ECalToEMGeVCalibration = ' + ECalToEMGeVCalibration + '\n'
configFileString += 'HCalToEMGeVCalibration = ' + HCalToEMGeVCalibration + '\n'
configFileString += 'ECalToHadGeVCalibration = ' + ECalToHadGeVCalibrationBarrel + '\n'
configFileString += 'HCalToHadGeVCalibration = ' + HCalToHadGeVCalibration + '\n'
configFileString += '\n'

configFileString += '# Pandora Threshold Cuts\n'
configFileString += 'ECalMIPThresholdPandora = ' + ECalMipThreshold + '\n'
configFileString += 'HCalMIPThresholdPandora = ' + HCalMipThreshold + '\n'
configFileString += '\n'

configFileString += '# Hadronic Energy Truncation in HCal PandoraPFA\n'
configFileString += 'MaxHCalHitHadronicEnergy = ' + MaxHCalHitHadronicEnergy + '\n'
configFileString += '\n'

configFileString += '# Timing ECal\n'
configFileString += 'ECalBarrelTimeWindowMax = ' + ECALBarrelTimeWindowMax + '\n'
configFileString += 'ECalEndcapTimeWindowMax = ' + ECALEndcapTimeWindowMax + '\n'
configFileString += '\n'

configFileString += '# Timing HCal\n'
configFileString += 'HCalBarrelTimeWindowMax = ' + HCALBarrelTimeWindowMax + '\n'
configFileString += 'HCalEndcapTimeWindowMax = ' + HCALEndcapTimeWindowMax
configFileString += '\n'

outputFile = open(sys.argv[2], 'w')
outputFile.write(configFileString)
outputFile.close()


