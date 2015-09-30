import sys
import os
import re

#fileName = 'MarlinSteeringFileTemplate_Jets_1.xml'
fileName = sys.argv[1]

newFileData = ''

PandoraSettingsFiles = {'Muon': 'PANDORASETTINGSMUON_XXXX', 'Default': 'PANDORASETTINGSDEFAULT_XXXX', 'PerfectPhoton': 'PANDORASETTINGSPERFECTPHOTON_XXXX', 'PerfectPhotonNK0L': 'PANDORASETTINGSPERFECTPHOTONNK0L_XXXX', 'PerfectPFA': 'PANDORASETTINGSPERFECTPFA_XXXX'}
RootFileOutputs = {'Muon': 'ROOTFILEMUON_XXXX', 'Default': 'ROOTFILEDEFAULT_XXXX', 'PerfectPhoton': 'ROOTFILEPERFECTPHOTON_XXXX', 'PerfectPhotonNK0L': 'ROOTFILEPERFECTPHOTONNK0L_XXXX', 'PerfectPFA': 'ROOTFILEPERFECTPFA_XXXX'}

key = ''

with open(fileName) as openFile:
    for line in openFile:
        if 'MyMarlinPandora' in line:
            matchObj = re.match('(.*?)"MyMarlinPandora(.*?)"(.*?)', line.strip(), re.M|re.I)
            if matchObj:
                key = matchObj.group(2)
        if 'PandoraSettingsXmlFile' in line:
            newFileData += '<parameter name="PandoraSettingsXmlFile" type="String">' + PandoraSettingsFiles[key] + '</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="PandoraSettingsXmlFile" type="String">' + PandoraSettingsFiles[key] + '</parameter>'
        elif '<!--processor name="MyLCIOOutputProcessor"/-->' in line:
            newFileData += '<processor name="MyLCIOOutputProcessor"/>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <processor name="MyLCIOOutputProcessor"/>'
        elif 'RootFile' in line and 'Digi' not in line:
            newFileData += '<parameter name="RootFile" type="string">' + RootFileOutputs[key] + '</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="RootFile" type="string">' + RootFileOutputs[key] + '</parameter>'
        elif 'GearXMLFile' in line:
            newFileData += '<parameter name="GearXMLFile" value="GEAR_FILE_XXXX"/>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="GearXMLFile" value="GEAR_FILE_XXXX"/>'
        elif 'LCIOInputFiles' in line:
            newFileData += '<parameter name="LCIOInputFiles">INPUT_SLCIO_FILE_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="LCIOInputFiles">INPUT_SLCIO_FILE_XXXX</parameter>'
        elif 'LCIOOutputFile' in line:
            newFileData += '<parameter name="LCIOOutputFile" type="string" >SLCIO_OUTPUT_FILE_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="LCIOOutputFile" type="string" >SLCIO_OUTPUT_FILE_XXXX</parameter>"/>'
        elif 'CalibrECAL' in line:
            newFileData += '<parameter name="CalibrECAL" type="FloatVec">CALIBR_ECAL_XXXX</parameter>\n' 
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibrECAL" type="FloatVec">CALIBR_ECAL_XXXX</parameter>'
        elif 'CalibrHCALBarrel' in line:
            newFileData += '<parameter name="CalibrHCALBarrel" type="FloatVec">CALIBR_HCAL_BARREL_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibrHCALBarrel" type="FloatVec">CALIBR_HCAL_BARREL_XXXX</parameter>'
        elif 'CalibrHCALEndcap' in line:
            newFileData += '<parameter name="CalibrHCALEndcap" type="FloatVec">CALIBR_HCAL_ENDCAP_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibrHCALEndcap" type="FloatVec">CALIBR_HCAL_ENDCAP_XXXX</parameter>'
        elif 'CalibrHCALOther' in line:
            newFileData += '<parameter name="CalibrHCALOther" type="FloatVec">CALIBR_HCAL_OTHER_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibrHCALOther" type="FloatVec">CALIBR_HCAL_OTHER_XXXX</parameter>'
        elif 'CalibrMUON' in line:
            newFileData += '<parameter name="CalibrMUON" type="FloatVec">CALIBR_MUON_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibrMUON" type="FloatVec">CALIBR_MUON_XXXX</parameter>'
        elif 'HCALBarrelTimeWindowMax' in line:
            newFileData += '<parameter name="HCALBarrelTimeWindowMax" type="float">HCALBARRELTIMEWINDOWMAX_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="HCALBarrelTimeWindowMax" type="float">HCALBARRELTIMEWINDOWMAX_XXXX</parameter>'
        elif 'HCALEndcapTimeWindowMax' in line:
            newFileData += '<parameter name="HCALEndcapTimeWindowMax" type="float">HCALENDCAPTIMEWINDOWMAX_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="HCALEndcapTimeWindowMax" type="float">HCALENDCAPTIMEWINDOWMAX_XXXX</parameter>'
        elif 'ECALBarrelTimeWindowMax' in line:
            newFileData += '<parameter name="ECALBarrelTimeWindowMax" type="float">ECALBARRELTIMEWINDOWMAX_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECALBarrelTimeWindowMax" type="float">ECALBARRELTIMEWINDOWMAX_XXXX</parameter>'
        elif 'ECALEndcapTimeWindowMax' in line:
            newFileData += '<parameter name="ECALEndcapTimeWindowMax" type="float">ECALENDCAPTIMEWINDOWMAX_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECALEndcapTimeWindowMax" type="float"> ECALENDCAPTIMEWINDOWMAX_XXXX </parameter>'
        elif 'CalibECALMIP' in line:
            newFileData += '<parameter name="CalibECALMIP" type="float">CALIBR_ECAL_MIP_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibECALMIP" type="float">CALIBR_ECAL_MIP_XXXX</parameter>'
        elif 'CalibHCALMIP' in line:
            newFileData += '<parameter name="CalibHCALMIP" type="float">CALIBR_HCAL_MIP_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="CalibHCALMIP" type="float">CALIBR_HCAL_MIP_XXXX</parameter>'
        elif 'ECalToMipCalibration' in line:
            newFileData += '<parameter name="ECalToMipCalibration" type="float">ECALTOMIPCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECalToMipCalibration" type="float">ECALTOMIPCALIBRATION_XXXX</parameter>'
        elif 'HCalToMipCalibration' in line:
            newFileData += '<parameter name="HCalToMipCalibration" type="float">HCALTOMIPCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="HCalToMipCalibration" type="float">HCALTOMIPCALIBRATION_XXXX</parameter>'
        elif 'MuonToMipCalibration' in line:
            newFileData += '<parameter name="MuonToMipCalibration" type="float">MUONTOMIPCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="MuonToMipCalibration" type="float">MUONTOMIPCALIBRATION_XXXX</parameter>'
        elif 'ECalMipThreshold' in line:
            newFileData += '<parameter name="ECalMipThreshold" type="float">ECALMIPTHRESHOLD_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECalMipThreshold" type="float">ECALMIPTHRESHOLD_XXXX</parameter>'
        elif 'HCalMipThreshold' in line:
            newFileData += '<parameter name="HCalMipThreshold" type="float">HCALMIPTHRESHOLD_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="HCalMipThreshold" type="float">HCALMIPTHRESHOLD_XXXX</parameter>'
        elif 'ECalToEMGeVCalibration' in line:
            newFileData += '<parameter name="ECalToEMGeVCalibration" type="float">ECALTOEMGEVCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECalToEMGeVCalibration" type="float">ECALTOEMGEVCALIBRATION_XXXX</parameter>'
        elif 'HCalToEMGeVCalibration' in line:
            newFileData += '<parameter name="HCalToEMGeVCalibration" type="float">HCALTOEMGEVCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="HCalToEMGeVCalibration" type="float">HCALTOEMGEVCALIBRATION_XXXX</parameter>'
        elif 'ECalToHadGeVCalibrationBarrel' in line:
            newFileData += '<parameter name="ECalToHadGeVCalibrationBarrel" type="float">ECALTOHADGEVCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECalToHadGeVCalibrationBarrel" type="float">ECALTOHADGEVCALIBRATION_XXXX</parameter>'
        elif 'ECalToHadGeVCalibrationEndCap' in line:
            newFileData += '<parameter name="ECalToHadGeVCalibrationEndCap" type="float">ECALTOHADGEVCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="ECalToHadGeVCalibrationEndCap" type="float">ECALTOHADGEVCALIBRATION_XXXX</parameter>'
        elif 'HCalToHadGeVCalibration' in line:
            newFileData += '<parameter name="HCalToHadGeVCalibration" type="float">HCALTOHADGEVCALIBRATION_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="HCalToHadGeVCalibration" type="float">HCALTOHADGEVCALIBRATION_XXXX</parameter>'
        elif 'MaxHCalHitHadronicEnergy' in line:
            newFileData += '<parameter name="MaxHCalHitHadronicEnergy" type="float">MAXHCALHITHADRONICENERGY_XXXX</parameter>\n'
            print 'Replacing : ' + line.strip()
            print 'with      : <parameter name="MaxHCalHitHadronicEnergy" type="float">MAXHCALHITHADRONICENERGY_XXXX</parameter>'
        else:
            newFileData += line

outputFile = open(fileName, 'w')
outputFile.write(newFileData)
outputFile.close()
