# Example to submit Marlin job: MarlinExample.py
import re

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.DiracILC import  DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *

# Marlin doesn't deal with I/O, just the streering files
#dirac = DiracILC(True,'repo.rep')

JobIdentificationString = 'Testing'
diracInstance = DiracILC( withRepo=True,
                          repoLocation="%s.cfg" %( JobIdentificationString)
                        )

#baseFileName = ''

#baseFile = open(baseFileName,'r')
#marlinSteeringTemplate = baseFile.read()
#baseFile.close()

ma = Marlin()
ma.setVersion('ILCSoft-01-17-07')
ma.setSteeringFile('ILD_o1_v06_5x5_30x30_uds91_00_0.xml')
ma.setGearFile('ILD_o1_v06_5x5_30x30.gear')
ma.setInputFile('lfn:/ilc/user/s/sgreen/MarlinTesting/ILD_o1_v06_uds91_00_0.slcio') # On grid need to match with job.setOutputData

# Job deals with I/O
job = UserJob()
job.setJobGroup('test')
job.setInputSandbox(['PandoraSettingsDefault_SiW_5x5.xml','PandoraLikelihoodData9EBin_SiW_5x5.xml']) # Local files
job.setOutputSandbox(['*.log','*.gear','*.mac','*.steer','*.xml'])
job.setOutputData(['Test2.root','Test2.slcio'],OutputPath='/MarlinTesting') # On grid
job.setName('TestJob2')
res = job.append(ma)

if not res['OK']:
  print res['Message']
  exit()
#job.submit(diracInstance)

### ----------------------------------------------------------------------------------------------------

def setPandoraSettingsFile(marlinSteeringTemplate,pandoraSettingsFile):
    marlinSteeringTemplate = re.sub('PANDORA_SETTINGS_XXXX',pandoraSettingsFile,marlinSteeringTemplate)
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
    marlinSteeringTemplate = re.sub('ROOT_OUTPUT_FILE_XXXX',outputFilePrefix + '.root',marlinSteeringTemplate)
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
    marlinSteeringTemplate = re.sub('ECALMIPMPV_XXXX',str(config['ECalMipMPV']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALMIPMPV_XXXX',str(config['HCalMIPMPV']),marlinSteeringTemplate)

    # MIP defintion post digitisation
    marlinSteeringTemplate = re.sub('ECALGEVTOMIP_XXXX',str(config['ECalToMIP']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALGEVTOMIP_XXXX',str(config['HCalToMIP']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('MUONGEVTOMIP_XXXX',str(config['MuonToMIP']),marlinSteeringTemplate)

    # MIP Threshold Cuts applied in Pandora
    marlinSteeringTemplate = re.sub('ECALMIPTHRESHOLD_XXXX',str(config['ECalMIPThresholdPandora']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALMIPTHRESHOLD_XXXX',str(config['HCalMIPThresholdPandora']),marlinSteeringTemplate)

    # Pandora PFA Calibration Constants
    # Electromagnetic
    marlinSteeringTemplate = re.sub('ECALTOEM_XXXX',str(config['ECalToEM']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALTOEM_XXXX',str(config['HCalToEM']),marlinSteeringTemplate)
    # Hadronic
    marlinSteeringTemplate = re.sub('ECALTOHAD_XXXX',str(config['ECalToHad']),marlinSteeringTemplate)
    marlinSteeringTemplate = re.sub('HCALTOHAD_XXXX',str(config['HCalToHad']),marlinSteeringTemplate)

    # Hadronic Corrections
    marlinSteeringTemplate = re.sub('MHHHE_XXXX',str(config['MaxHCalHitHadronicEnergy']),marlinSteeringTemplate)

    return marlinSteeringTemplate

### ----------------------------------------------------------------------------------------------------

marlinSteeringTemplate = ''
marlinSteeringTemplate = getMarlinSteeringFileTemplate('baseFileName.xml','CalibrationConfig.py')
marlinSteeringTemplate = setPandoraSettingsFile(marlinSteeringTemplate,'PandoraSettings.xml')
marlinSteeringTemplate = setGearFile(marlinSteeringTemplate,'ILD_o1_v06_5x5_30x30.gear')
marlinSteeringTemplate = setInputSlcioFile(marlinSteeringTemplate,'ILD_o1_v06_uds91_00_0.slcio')
marlinSteeringTemplate = setOutputFiles(marlinSteeringTemplate,'Test3')

text_file = open("Output.xml", "w")
text_file.write(marlinSteeringTemplate)
text_file.close()
