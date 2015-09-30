# Calibration config file for testing
# Digitisation Constants - ECal 
CalibrECal = 42.3662496409

# Digitisation Constants - HCal
CalibrHCalBarrel = 50.3504586994
CalibrHCalEndcap = 55.6419000329
CalibrHCALOther = 30.5873671511

# Digitisation Constants - Muon Chamber
CalibrMuon = 56.7

# MIP Peak position in directed corrected SimCaloHit energy distributions
# used for realistic ECal and HCal digitisation options
CalibrECalMIP = 0.0001475
CalibrHCalMIP = 0.0004925

# MIP Peak position in directed corrected CaloHit energy distributions
# used for MIP definition in PandoraPFA
ECalToMIPCalibration = 153.846
HCalToMIPCalibration = 36.1011
MuonToMIPCalibration = 10.101

# EM and Had Scale Settings
ECalToEMGeVCalibration = 1.00191662289
HCalToEMGeVCalibration = 1.00191662289
ECalToHadGeVCalibration = 1.110382899
HCalToHadGeVCalibration = 1.06424468744

# Pandora Threshold Cuts
ECalMIPThresholdPandora = 0.5
HCalMIPThresholdPandora = 0.3

# Hadronic Energy Truncation in HCal PandoraPFA
MaxHCalHitHadronicEnergy = 2.0

# Timing ECal
ECalBarrelTimeWindowMax = 300.0
ECalEndcapTimeWindowMax = 300.0

# Timing HCal
HCalBarrelTimeWindowMax = 300.0
HCalEndcapTimeWindowMax = 300.0
