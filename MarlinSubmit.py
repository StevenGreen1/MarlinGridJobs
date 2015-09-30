# Example to submit Marlin job: MarlinExample.py
import os
import sys

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from ILCDIRAC.Interfaces.API.DiracILC import  DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.NewInterface.Applications import *

from MarlinGridJobs import *

JobIdentificationString = 'Testing'
diracInstance = DiracILC(withRepo=True,repoLocation="%s.cfg" %( JobIdentificationString))

#===== User Input =====

mokkaJobNumber = 38
energy = ['1','2','3','4','5','6','7','8','9','10','15','20','25','30','35','40','45','50']
eventType = ['Kaon0L']

baseXmlFile = ''

pandoraSettingsFiles = {}
pandoraSettingsFiles['Default'] = '' 
pandoraSettingsFiles['Default_LikelihoodData'] = '' 
pandoraSettingsFiles['Muon'] = ''
pandoraSettingsFiles['PerfectPhoton'] = ''
pandoraSettingsFiles['PerfectPhotonNK0L'] = ''
pandoraSettingsFiles['PerfectPFA'] = ''

gearFile = 'ILD_o1_v06_5x5_30x30.gear'

calibConfigFile = 'CalibrationConfig.py'

#=====

slcioFilesToProcess = getSlcioFiles(mokkaJobNumber, energy, eventType)

for slcioFile in slcioFilesToProcess:
    marlinSteeringTemplate = ''
    marlinSteeringTemplate = getMarlinSteeringFileTemplate('baseFileName.xml',calibConfigFile)
    marlinSteeringTemplate = setPandoraSettingsFile(marlinSteeringTemplate,pandoraSettingsFiles)
    marlinSteeringTemplate = setGearFile(marlinSteeringTemplate,gearFile)

    slcioFileNoPath = os.path.basename(slcioFile)
    #print slcioFileNoPath
    #print slcioFileNoPath[:-6]

    marlinSteeringTemplate = setInputSlcioFile(marlinSteeringTemplate,slcioFileNoPath)
    marlinSteeringTemplate = setOutputFiles(marlinSteeringTemplate,'MarlinReco_' + slcioFileNoPath[:-6])

    with open("MarlinSteering.steer" ,"w") as SteeringFile:
        SteeringFile.write(marlinSteeringTemplate)

    ma = Marlin()
    ma.setVersion('ILCSoft-01-17-07')
    ma.setSteeringFile('MarlinSteering.steer')
    ma.setGearFile(gearFile)
    ma.setInputFile('lfn:' + slcioFile)

    outputRootFile = 'MarlinReco_' + slcioFileNoPath[:-6] + '.root'
    outputSlcioFile = 'MarlinReco_' + slcioFileNoPath[:-6] + '.slcio'

    job = UserJob()
    job.setJobGroup('test')
    job.setInputSandbox(pandoraSettingsFiles.values()) # Local files
    job.setOutputSandbox(['*.log','*.gear','*.mac','*.steer','*.xml'])
    job.setOutputData([outputRootFile,outputSlcioFile],OutputPath='/MarlinTesting') # On grid
    job.setName('Testing')
    #job.dontPromptMe()
    res = job.append(ma)

    if not res['OK']:
        print res['Message']
        exit()
    job.submit(diracInstance)

# Tidy Up
os.system('rm MarlinSteering.steer')

