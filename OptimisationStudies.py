import os

### ----------------------------------------------------------------------------------------------------
### Start of getListOfFiles
### ----------------------------------------------------------------------------------------------------

#def getListOfFiles(gridJobNumber, energy):
mokkaJobNumber = 45 
gearFile = '/r04/lc/sg568/HCAL_Optimisation_Studies/GridSandboxes/GJN' + str(mokkaJobNumber) + '_OutputSandbox/ILD_o1_v06_GJN' + str(mokkaJobNumber) + '.gear'
pandoraSettingsFiles = []

JobIdentificationString = 'OptimisationStudiesBatch'
diracInstance = DiracILC( withRepo=True,
                          repoLocation="%s.cfg" %( JobIdentificationString)
                        )

ma = Marlin()
ma.setVersion('ILCSoft-01-17-07')
ma.setSteeringFile('ILD_o1_v06_5x5_30x30_uds91_00_0.xml')
ma.setGearFile('ILD_o1_v06_5x5_30x30.gear')
ma.setInputFile('lfn:/ilc/user/s/sgreen/MarlinTesting/ILD_o1_v06_uds91_00_0.slcio')

for eventType in ['Kaon0L']:
    for energy in ['10']:
        os.system('dirac-ilc-find-in-FC /ilc MokkaJobNumber=' + str(mokkaJobNumber) + ' Energy=' + str(energy) + ' Type="' + eventType + '" > tmp.txt')
        with open('tmp.txt') as f:
            lines = f.readlines()
            for idx, line in enumerate(lines):
                line = line.strip()
                print line

#    if gridJobNumber == 38:
#        if energy == 91:
#            gridJobMokkaPath = '/ilc/user/s/sgreen/0804/HCalStudiessg568/GJN38/Z_uds/91GeV/00/ILD_o1_v06_GJN38_uds91_01_0.slcio'
#            list.append(subList)
#        list=[ {'name':'/ilc/prod/clic/91gev/Z_uds/gen/0/00.stdhep', 'nEvents': 1000, 'eventType': 'Z_uds'},
#                   {'name':'/ilc/prod/clic/91gev/Z_uds/gen/0/09.stdhep', 'nEvents': 1000, 'eventType': 'Z_uds'}]
#    return list
