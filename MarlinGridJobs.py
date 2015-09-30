# Example to submit Marlin job: MarlinExample.py
import re
import os

### ----------------------------------------------------------------------------------------------------

def setPandoraSettingsFile(marlinSteeringTemplate,pandoraSettingsFiles):
    marlinSteeringTemplate = re.sub('PANDORASETTINGSDEFAULT_XXXX',pandoraSettingsFiles['Default'],marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('PANDORASETTINGSMUON_XXXX',pandoraSettingsFiles['Muon'],marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('PANDORASETTINGSPERFECTPHOTON_XXXX',pandoraSettingsFiles['PerfectPhoton'],marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('PANDORASETTINGSPERFECTPHOTONNK0L_XXXX',pandoraSettingsFiles['PerfectPhotonNK0L'],marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('PANDORASETTINGSPERFECTPFA_XXXX',pandoraSettingsFiles['PerfectPFA'],marlinSteeringTemplate)
    return marlinSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def setGearFile(marlinSteeringTemplate,gearFile):
    marlinSteeringTemplate = re.sub('GEAR_FILE_XXXX',gearFile,marlinSteeringTemplate)
    return marlinSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def setInputSlcioFile(marlinSteeringTemplate,inputSlcioFile):
    marlinSteeringTemplate = re.sub('INPUT_SLCIO_FILE_XXXX',inputSlcioFile,marlinSteeringTemplate)
    return marlinSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def setOutputFiles(marlinSteeringTemplate,outputFilePrefix):
    marlinSteeringTemplate = re.sub('ROOTFILEDEFAULT_XXXX',outputFilePrefix + '_Default.root',marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('ROOTFILEMUON_XXXX',outputFilePrefix + '_Muon.root',marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('ROOTFILEPERFECTPHOTON_XXXX',outputFilePrefix + '_PerfectPhoton.root',marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('ROOTFILEPERFECTPHOTONNK0L_XXXX',outputFilePrefix + '_PerfectPhotonNK0L.root',marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('ROOTFILEPERFECTPFA_XXXX',outputFilePrefix + '_PerfectPFA.root',marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('SLCIO_OUTPUT_FILE_XXXX',outputFilePrefix + '.slcio',marlinSteeringTemplate)
    return marlinSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def getMarlinSteeringFileTemplate(baseFileName,calibrationFileName):
    config = {}
    execfile(calibrationFileName, config)

    baseFile = open(baseFileName,'r')
    marlinSteeringTemplate = baseFile.read()
    baseFile.close()

    # Digitisation Constants
    ECalString = str(config['CalibrECal']) + ' ' + str(2 * config['CalibrECal'])
    marlinSteeringTemplate = re.sub('CALIBR_ECAL_XXXX',ECalString,marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('CALIBR_HCAL_BARREL_XXXX',str(config['CalibrHCalBarrel']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('CALIBR_HCAL_ENDCAP_XXXX',str(config['CalibrHCalEndcap']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('CALIBR_HCAL_OTHER_XXXX',str(config['CalibrHCALOther']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('CALIBR_MUON_XXXX',str(config['CalibrMuon']),marlinSteeringTemplate)

    # Timing Cuts in HCal
    marlinSteeringTemplate = re.sub('HCALBARRELTIMEWINDOWMAX_XXXX',str(config['HCalBarrelTimeWindowMax']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALENDCAPTIMEWINDOWMAX_XXXX',str(config['HCalEndcapTimeWindowMax']),marlinSteeringTemplate)

    # Timing Cuts in ECal
    marlinSteeringTemplate = re.sub('ECALBARRELTIMEWINDOWMAX_XXXX',str(config['ECalBarrelTimeWindowMax']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('ECALENDCAPTIMEWINDOWMAX_XXXX',str(config['ECalEndcapTimeWindowMax']),marlinSteeringTemplate)

    # MIP definition pre digitisation
    marlinSteeringTemplate = re.sub('CALIBR_ECAL_MIP_XXXX',str(config['CalibrECalMIP']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('CALIBR_HCAL_MIP_XXXX',str(config['CalibrHCalMIP']),marlinSteeringTemplate)

    # MIP defintion post digitisation
    marlinSteeringTemplate = re.sub('ECALTOMIPCALIBRATION_XXXX',str(config['ECalToMIPCalibration']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALTOMIPCALIBRATION_XXXX',str(config['HCalToMIPCalibration']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('MUONTOMIPCALIBRATION_XXXX',str(config['MuonToMIPCalibration']),marlinSteeringTemplate)

    # MIP Threshold Cuts applied in Pandora
    marlinSteeringTemplate = re.sub('ECALMIPTHRESHOLD_XXXX',str(config['ECalMIPThresholdPandora']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALMIPTHRESHOLD_XXXX',str(config['HCalMIPThresholdPandora']),marlinSteeringTemplate)

    # Pandora PFA Calibration Constants
    # Electromagnetic
    marlinSteeringTemplate = re.sub('ECALTOEMGEVCALIBRATION_XXXX',str(config['ECalToEMGeVCalibration']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALTOEMGEVCALIBRATION_XXXX',str(config['HCalToEMGeVCalibration']),marlinSteeringTemplate)
    # Hadronic
    marlinSteeringTemplate = re.sub('ECALTOHADGEVCALIBRATION_XXXX',str(config['ECalToHadGeVCalibration']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALTOHADGEVCALIBRATION_XXXX',str(config['HCalToHadGeVCalibration']),marlinSteeringTemplate)

    # Hadronic Corrections
    marlinSteeringTemplate = re.sub('MAXHCALHITHADRONICENERGY_XXXX',str(config['MaxHCalHitHadronicEnergy']),marlinSteeringTemplate)

    return marlinSteeringTemplate

### ----------------------------------------------------------------------------------------------------

def getSlcioFiles(mokkaJobNumber, energy, eventType):
    slcioFiles = []
    os.system('dirac-ilc-find-in-FC /ilc MokkaJobNumber=' + str(mokkaJobNumber) + ' Energy=' + str(energy) + ' Type="' + eventType + '" > tmp.txt')
    with open('tmp.txt') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            line = line.strip()
            slcioFiles.append(line)
    os.system('rm tmp.txt')
    return slcioFiles

### ----------------------------------------------------------------------------------------------------

