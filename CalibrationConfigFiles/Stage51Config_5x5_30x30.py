# Calibration config file for testing
# Digitisation Constants - ECal 
CalibrECal = 42.4006899902

# Digitisation Constants - HCal
CalibrHCalBarrel = 51.3986461682
CalibrHCalEndcap = 56.3645119191
CalibrHCALOther = 29.8292431092

# Digitisation Constants - Muon Chamber
CalibrMuon = 56.7

# MIP Peak position in directed corrected SimCaloHit energy distributions
# used for realistic ECal and HCal digitisation options
CalibrECalMIP = 0.0001475
CalibrHCalMIP = 0.0004925

# MIP Peak position in directed corrected CaloHit energy distributions
# used for MIP definition in PandoraPFA
ECalToMIPCalibration = 153.846
HCalToMIPCalibration = 36.9004
MuonToMIPCalibration = 10.101

# EM and Had Scale Settings
ECalToEMGeVCalibration = 1.00162645296
HCalToEMGeVCalibration = 1.00162645296
ECalToHadGeVCalibration = 1.17258504222
HCalToHadGeVCalibration = 1.05357620948

# Pandora Threshold Cuts
ECalMIPThresholdPandora = 0.5
HCalMIPThresholdPandora = 0.3

# Hadronic Energy Truncation in HCal PandoraPFA
MaxHCalHitHadronicEnergy = 1000000.0

# Timing ECal
ECalBarrelTimeWindowMax = 10.0
ECalEndcapTimeWindowMax = 10.0

# Timing HCal
HCalBarrelTimeWindowMax = 10.0
HCalEndcapTimeWindowMax = 10.0
