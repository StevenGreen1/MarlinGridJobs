import os

from DIRAC.Core.Base import Script
Script.parseCommandLine()
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

# Correctly assigns data for GJN38 to GJN45
def runOne ():
    fc = FileCatalogClient()
    for mokkaJobNumber in range(39,45):
        for eventType in ['Z_uds','Photon','Kaon0L','Muon']:
            energies = []
            if eventType == 'Z_uds':
                energies = [91,200,360,500,750,1000,2000,3000]
            elif eventType == 'Photon':
                energies = [10]
            elif eventType == 'Muon':
                energies = [10]
            elif eventType == 'Kaon0L':
                energies = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]
            for energy in energies:
                path = '/ilc/user/s/sgreen/0804/HCalStudiessg568/GJN' + str(mokkaJobNumber) + '/' + eventType + '/' + str(energy) + 'GeV'
                pathdict = {'path':path, 'meta':{'MokkaJobNumber':mokkaJobNumber, 'Type':eventType, 'Energy':energy}}
                res = fc.setMetadata(pathdict['path'], pathdict['meta'])
    return

cities = {
    'CA': 'San Francisco',
    'MI': 'Detroit',
    'FL': 'Jacksonville'
}

mokkaFilePath = {
    45 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN45/GJN45',
    46 : '/ilc/user/s/sgreen/0804HP/HCalStudies_GJN45_GJN46/GJN46',
    47 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN45_GJN46_GJN47/GJN47',
    48 : '/ilc/user/s/sgreen/0804HP/HCalStudies_GJN45_GJN46_GJN47_GJN48/GJN48',
    49 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49/GJN49',
    50 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49_GJN50/GJN50',
    51 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49_GJN50_GJN51/GJN51',
    52 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49_GJN50_GJN51_GJN52/GJN52',
    53 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49_GJN50_GJN51_GJN52_GJN53/GJN53',
    54 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49_GJN50_GJN51_GJN52_GJN53_GJN54/GJN54',
    55 : '/ilc/user/s/sgreen/0804/HCalStudies_GJN49/GJN50_GJN51_GJN52_GJN53_GJN54_GJN55/GJN55'
}

for i in range(56,78):
    mokkaFilePath[i] = '/ilc/user/s/sgreen/0804/HCalStudies_GJN' + str(i) + '/GJN' + str(i)


fc = FileCatalogClient()
for mokkaJobNumber in range(45,78):
   for eventType in ['Z_uds','Photon','Kaon0L','Muon']:
        energies = []
        if eventType == 'Z_uds':
            energies = [91,200,360,500,750,1000,2000,3000]
        elif eventType == 'Photon':
            energies = [10]
        elif eventType == 'Muon':
            energies = [10]
        elif eventType == 'Kaon0L':
            energies = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]
        for energy in energies:
            path = os.path.join(mokkaFilePath[mokkaJobNumber], eventType + '/' + str(energy) + 'GeV')
            pathdict = {'path':path, 'meta':{'MokkaJobNumber':mokkaJobNumber, 'Type':eventType, 'Energy':energy}}
#            print pathdict
            res = fc.setMetadata(pathdict['path'], pathdict['meta'])


#meta = {}
#meta['MokkaJobNumber'] = '38' 
#meta['Energy'] = '91'
#meta['Type'] = 'Z_uds'

#res = fc.findFilesByMetadata(meta)
#if not res['OK']:
#   print res['Message']

#lfns = res['Value']

#print "Found %s files" % len(lfns)
#for lfn in lfns:
#   print lfn
