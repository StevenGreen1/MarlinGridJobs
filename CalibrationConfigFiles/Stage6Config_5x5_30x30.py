# Calibration config file for testing
# Digitisation Constants - ECal 
CalibrECal = 42.4925238195

# Digitisation Constants ILDCaloDigi - HCal
CalibrHCalBarrel = 52.8844697272
CalibrHCalEndcap = 59.5569513399
CalibrHCalOther = 33.0005470630

# Digitisation Constants NewLDCCaloDigi - HCal
CalibrHCal = -1

# Digitisation Constants - Muon Chamber
CalibrMuon = 56.7

# MIP Peak position in directed corrected SimCaloHit energy distributions
# used for realistic ECal and HCal digitisation options
CalibrECalMIP = -1
CalibrHCalMIP = -1

# MIP Peak position in directed corrected CaloHit energy distributions
# used for MIP definition in PandoraPFA
ECalToMIPCalibration = 158.73
HCalToMIPCalibration = 36.63
MuonToMIPCalibration = 10.101

# EM and Had Scale Settings
ECalToEMGeVCalibration = 0.999700939889
HCalToEMGeVCalibration = 0.999700939889
ECalToHadGeVCalibration = 1.15100975333
HCalToHadGeVCalibration = 1.06717254302

# Pandora Threshold Cuts
ECalMIPThresholdPandora = 0.5
HCalMIPThresholdPandora = 0.3

# Hadronic Energy Truncation in HCal PandoraPFA
MaxHCalHitHadronicEnergy = 1

# Timing ECal
ECalBarrelTimeWindowMax = 10.0
ECalEndcapTimeWindowMax = 10.0

# Timing HCal
HCalBarrelTimeWindowMax = 10.0
HCalEndcapTimeWindowMax = 10.0
