# Example to submit Marlin job: MarlinExample.py
import os
import sys

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.DiracILC import  DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *

from MarlinGridJobs import *

#===== User Input =====

gridJobNumber = 38 # Default detector model
recoStageNumber = 36 

eventsToSimulate = [ #{ 'EventType': "Kaon0L"  , 'Energies':  ['1','2','3','4','5','6','7','8','9','10','15','20','25','30','35','40','45','50'] }
                     #{ 'EventType': "Z_uds"   , 'Energies':  [91, 200, 360, 500, 750, 1000, 2000, 3000]                                         },
                     #{ 'EventType': "Photon"  , 'Energies':  [10]                                                                               },
                     { 'EventType': "Kaon0L"  , 'Energies':  ['1']                                                                               }
                     #{ 'EventType': "Muon"    , 'Energies':  [10]                                                                               }
                   ]

baseXmlFile = 'TemplateRepository/MarlinSteeringFileTemplate_SingleParticles_1.xml'

pandoraSettingsFiles = {}
pandoraSettingsFiles['Default'] = 'PandoraSettings/PandoraSettingsDefault_SiW_5x5.xml' 
pandoraSettingsFiles['Default_LikelihoodData'] = 'PandoraSettings/PandoraLikelihoodData9EBin_SiW_5x5.xml' 
pandoraSettingsFiles['Muon'] = 'PandoraSettings/PandoraSettingsMuon.xml'
pandoraSettingsFiles['PerfectPhoton'] = 'PandoraSettings/PandoraSettingsPerfectPhoton.xml'
pandoraSettingsFiles['PerfectPhotonNK0L'] = 'PandoraSettings/PandoraSettingsPerfectPhotonNeutronK0L.xml'
pandoraSettingsFiles['PerfectPFA'] = 'PandoraSettings/PandoraSettingsPerfectPFA.xml'

#===== Second level user input =====
# If using naming scheme doesn't need changing 

gearFile = '/r04/lc/sg568/HCAL_Optimisation_Studies/GridSandboxes/GJN' + str(gridJobNumber) + '_OutputSandbox/ILD_o1_v06_GJN' + str(gridJobNumber) + '.gear'
calibConfigFile = 'CalibrationConfigFiles/Stage' + str(recoStageNumber) + 'Config_5x5_30x30.py'

#=====

# Copy gear file and pandora settings files to local directory as is needed for submission.
os.system('cp ' + gearFile + ' .')
gearFileLocal = os.path.basename(gearFile)

pandoraSettingsFilesLocal = {}
for key, value in pandoraSettingsFiles.iteritems():
    os.system('cp ' + value + ' .')
    pandoraSettingsFilesLocal[key] = os.path.basename(value)

# Start submission
JobIdentificationString = 'ReviewJER_Detector_' + str(gridJobNumber) + '_Reco_' + str(recoStageNumber)
diracInstance = DiracILC(withRepo=True,repoLocation="%s.cfg" %( JobIdentificationString))

for eventSelection in eventsToSimulate:
    eventType = eventSelection['EventType']
    for energy in eventSelection['Energies']:
        slcioFilesToProcess = getSlcioFiles(gridJobNumber, energy, eventType)
        #print slcioFilesToProcess
        for slcioFile in slcioFilesToProcess:
            marlinSteeringTemplate = ''
            marlinSteeringTemplate = getMarlinSteeringFileTemplate(baseXmlFile,calibConfigFile)
            marlinSteeringTemplate = setPandoraSettingsFile(marlinSteeringTemplate,pandoraSettingsFilesLocal)
            marlinSteeringTemplate = setGearFile(marlinSteeringTemplate,gearFileLocal)

            slcioFileNoPath = os.path.basename(slcioFile)
            marlinSteeringTemplate = setInputSlcioFile(marlinSteeringTemplate,slcioFileNoPath)
            marlinSteeringTemplate = setOutputFiles(marlinSteeringTemplate,'MarlinReco_' + slcioFileNoPath[:-6])

            with open("MarlinSteering.steer" ,"w") as SteeringFile:
                SteeringFile.write(marlinSteeringTemplate)

            ma = Marlin()
            ma.setVersion('ILCSoft-01-17-07')
            ma.setSteeringFile('MarlinSteering.steer')
            ma.setGearFile(gearFileLocal)
            ma.setInputFile('lfn:' + slcioFile)

            outputFiles = []
            outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_Default.root')
            outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '.slcio')
            if eventType == 'Z_uds':
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_Muon.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPhoton.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPhotonNK0L.root')
                outputFiles.append('MarlinReco_' + slcioFileNoPath[:-6] + '_PerfectPFA.root')

            job = UserJob()
            job.setJobGroup('ReviewJER')
            job.setInputSandbox(pandoraSettingsFilesLocal.values()) # Local files
            job.setOutputSandbox(['*.log','*.gear','*.mac','*.steer','*.xml'])
            job.setOutputData(outputFiles,OutputPath='/ReviewJER/MarlinJobs/Detector_Model_' + str(gridJobNumber) + '/Reco_Stage_' + str(recoStageNumber) + '/' + eventType + '/' + energy + 'GeV') # On grid
            job.setName('ReviewJER_Detector' + str(gridJobNumber) + '_Reco_' + str(recoStageNumber))
            job.dontPromptMe()
            res = job.append(ma)

            if not res['OK']:
                print res['Message']
                exit()
            job.submit(diracInstance)
            os.system('rm *.cfg')

# Tidy Up
os.system('rm MarlinSteering.steer')
os.system('rm ' + gearFileLocal)
for key, value in pandoraSettingsFilesLocal.iteritems():
    os.system('rm ' + value)

