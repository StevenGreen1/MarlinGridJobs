# Calibration config file for testing
# Digitisation Constants - ECal 
CalibrECal = 42.4326603502 84.8653207004

# Digitisation Constants - HCal
CalibrHCalBarrel = 49.057884929
CalibrHCalEndcap = 54.1136311832
CalibrHCALOther = 29.2180288685

# Digitisation Constants - Muon Chamber
CalibrMuon = 56.7

# MIP Peak position in directed corrected SimCaloHit energy distributions
# used for realistic ECal and HCal digitisation options
CalibrECalMIP = -1
CalibrHCalMIP = 0.0004925

# MIP Peak position in directed corrected CaloHit energy distributions
# used for MIP definition in PandoraPFA
ECalToMIPCalibration = 158.73
HCalToMIPCalibration = 40.8163
MuonToMIPCalibration = 10.101

# EM and Had Scale Settings
ECalToEMGeVCalibration = 1.00062470217
HCalToEMGeVCalibration = 1.00062470217
ECalToHadGeVCalibration = 1.02363721072
HCalToHadGeVCalibration = 1.26439608145

# Pandora Threshold Cuts
ECalMIPThresholdPandora = 0.5
HCalMIPThresholdPandora = 0.3

# Hadronic Energy Truncation in HCal PandoraPFA
MaxHCalHitHadronicEnergy = 0.5

# Timing ECal
ECalBarrelTimeWindowMax = 1000000.0
ECalEndcapTimeWindowMax = 1000000.0

# Timing HCal
HCalBarrelTimeWindowMax = 1000000.0
HCalEndcapTimeWindowMax = 1000000.0
