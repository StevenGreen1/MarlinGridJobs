# Calibration config file for testing
# Digitisation Constants - ECal 
CalibrECal = 42.4520342634

# Digitisation Constants - HCal
CalibrHCalBarrel = 49.1710071886
CalibrHCalEndcap = 53.4569694414
CalibrHCALOther = 28.2164381239

# Digitisation Constants - Muon Chamber
CalibrMuon = 56.7

# MIP Peak position in directed corrected SimCaloHit energy distributions
# used for realistic ECal and HCal digitisation options
CalibrECalMIP = -1
CalibrHCalMIP = -1

# MIP Peak position in directed corrected CaloHit energy distributions
# used for MIP definition in PandoraPFA
ECalToMIPCalibration = 158.73
HCalToMIPCalibration = 39.8406
MuonToMIPCalibration = 10.101

# EM and Had Scale Settings
ECalToEMGeVCalibration = 1.00022115946
HCalToEMGeVCalibration = 1.00022115946
ECalToHadGeVCalibration = 1.10452372966
HCalToHadGeVCalibration = 1.06418928754

# Pandora Threshold Cuts
ECalMIPThresholdPandora = 0.5
HCalMIPThresholdPandora = 0.3

# Hadronic Energy Truncation in HCal PandoraPFA
MaxHCalHitHadronicEnergy = 10.0

# Timing ECal
ECalBarrelTimeWindowMax = 1000000.0
ECalEndcapTimeWindowMax = 1000000.0

# Timing HCal
HCalBarrelTimeWindowMax = 1000000.0
HCalEndcapTimeWindowMax = 1000000.0
