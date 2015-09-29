import os

class HCalSubmission:
    """Class to hold all the information to submit Mokka jobs to the grid"""
    _MokkaVersion               = ""
    _JobIdentificationString    = ""
    _EventsPerJob               = 100
    _GeometryAdaption           = ""
    _EventSelection             = []
    _MaxNumberOfJobs            = -1
    _PhysicsList                = ""
    _HCalAbsorberMaterial       = ""
    _HCalAbsorberLayerThickness = 0
    _HCalScintillatorThickness  = 0
    _CoilExtraSize              = 0
    _DetailedShowerMode         = ""
    _Identifier                 = ""
    _NumberHCalLayers           = 0
    _BField                     = 0
    _TPCOuterRadius             = 0
    _HCalCellSize               = 0
    _DetectorModel              = ""
    _debug                      = False
    _DiracInstance              = 0
    _NumberOfJobInList          = -1
        

### ----------------------------------------------------------------------------------------------------
### Constructor with choosable values
### ----------------------------------------------------------------------------------------------------
    def __init__(self,
               MokkaVersion                 = "0804",
               JobIdentificationString      = "HCalSimulation",
               EventsPerJob                 = 100,
               GeometryAdaption             = "",
               EventSelection               = [],
               MaxNumberOfJobs              = -1,
               PhysicsList                  = "",
               HCalAbsorberMaterial         = "",
               HCalAbsorberLayerThickness   = 0,
               HCalScintillatorThickness    = 0,
               CoilExtraSize                = 0,
               DetailedShowerMode           = "",
               Identifier                   = "",
               NumberHCalLayers             = 0,
               BField                       = 0,
               TPCOuterRadius               = 0,
               HCalCellSize                 = 0,
               DetectorModel                = "",
               NumberOfJobInList            = -1):
        self._MokkaVersion                  = MokkaVersion
        self._JobIdentificationString       = JobIdentificationString
        self._EventsPerJob                  = EventsPerJob
        self._GeometryAdaption              = GeometryAdaption
        self.setEventSelection(EventSelection)
        self._MaxNumberOfJobs               = MaxNumberOfJobs
        self._PhysicsList                   = PhysicsList
        self._HCalAbsorberMaterial          = HCalAbsorberMaterial
        self._HCalAbsorberLayerThickness    = HCalAbsorberLayerThickness
        self._HCalScintillatorThickness     = HCalScintillatorThickness
        self._CoilExtraSize                 = CoilExtraSize
        self._DetailedShowerMode            = DetailedShowerMode
        self._Identifier                    = Identifier
        self._NumberHCalLayers              = NumberHCalLayers
        self._BField                        = BField
        self._TPCOuterRadius                = TPCOuterRadius
        self._HCalCellSize                  = HCalCellSize
        self._DetectorModel                 = DetectorModel
        self._debug                         = False
        self._dryRun                        = False
        self._NumberOfJobInList             = NumberOfJobInList  
        from ILCDIRAC.Interfaces.API.DiracILC import DiracILC

        self._DiracInstance           = DiracILC( withRepo=True,
                                                  repoLocation="%s.cfg" %( JobIdentificationString)
                                                  )
### ----------------------------------------------------------------------------------------------------
### End of Constructor
### ----------------------------------------------------------------------------------------------------
### Start of setEventSelection function
### ----------------------------------------------------------------------------------------------------
    def setEventSelection(self, EventSelection):
        try:
            for d in EventSelection:
                EventType = d['EventType']
                for Energy in d['Energies']:
                    getListOfFiles(EventType, Energy)
                    
            ## If there was no exception
            self._EventSelection = EventSelection

        except Exception as e:
            print "setEventSelection -- ERROR:", str(e)
            raise e
### ----------------------------------------------------------------------------------------------------
### End of setEventSelection function
### ----------------------------------------------------------------------------------------------------
### Start of submitJons function
### ----------------------------------------------------------------------------------------------------
    def submitJobs(self):
        from ILCDIRAC.Interfaces.API.NewInterface.UserJob import  UserJob
        from ILCDIRAC.Interfaces.API.NewInterface.Applications import Mokka
        from DIRAC import gLogger
        JobCounter = -1
        print "Submitting jobs..."
        for d in self._EventSelection:
            EventType = d['EventType']
            for Energy in d['Energies']:
                FileNumber = 0
                for MyFile in getAFiles(EventType, Energy, self._NumberOfJobInList): 
                    EventsPerFile = MyFile['nEvents']
                    FileLFN = MyFile['name']
                    EventType = MyFile['eventType']
                    EventsPerJob = self._EventsPerJob
                    FileFNname =  os.path.splitext(os.path.basename(FileLFN))[0]
                    if 'MaxNumberOfEvents' in MyFile:
                        EventsPerJob = MyFile['MaxNumberOfEvents']

                    FileNumber += 1
                    MyOutputPath="%s/%s/%s/%s/%dGeV/%s" %( self._MokkaVersion, 
                                                     self._JobIdentificationString, 
                                                     self._Identifier,
                                                     EventType, 
                                                     Energy,
                                                     FileFNname)

                    if self._debug:
                        print EventType, FileLFN, FileNumber
                    for StartEvent in xrange(0, EventsPerFile, EventsPerJob):
                        JobCounter += 1
                        if self._MaxNumberOfJobs == -1 or JobCounter < self._MaxNumberOfJobs:
                            from sys import stdout
                            stdout.write( '\rSubmitting Job Number: %d' % (JobCounter) )
                            
### Example %02d tells code to use zeros in string e.g. '%04d' % 2 is 0002
                            if EventType == "Z_uds":
                                MyOutputFilename="%s_%s_uds%d_%02d_%d.slcio" % ( self._DetectorModel,
                                                                                      self._Identifier, 
                                                                                      Energy, 
                                                                                      FileNumber, 
                                                                                      StartEvent
                                                                                )
                            elif EventType == "Kaon0L":
                                MyOutputFilename="%s_%s_%d_GeV_Energy_130_pdg_SN_%d.slcio" % ( self._DetectorModel,
                                                                                               self._Identifier, 
                                                                                               Energy, 
                                                                                               FileNumber
                                                                                             )
                            elif EventType == "Photon":
                                MyOutputFilename="%s_%s_%d_GeV_Energy_22_pdg_SN_%d.slcio" % ( self._DetectorModel,
                                                                                              self._Identifier, 
                                                                                              Energy, 
                                                                                              FileNumber
                                                                                            )
                            elif EventType == "Muon":
                                MyOutputFilename="%s_%s_%d_GeV_Energy_13_pdg_SN_%d.slcio" % ( self._DetectorModel,
                                                                                              self._Identifier, 
                                                                                              Energy, 
                                                                                              FileNumber
                                                                                            )
                            else:
                                MyOutputFilename="%s_%s_%d_GeV_Energy_" + EventType + "_%02d_%d.slcio" %    ( self._DetectorModel,
                                                                                                              self._Identifier, 
                                                                                                              Energy, 
                                                                                                              FileNumber, 
                                                                                                              StartEvent
                                                                                                            )

                            MyGearOutputFilename="%s_%s.gear" % ( self._DetectorModel,
                                                                  self._Identifier )
### Example string substitution:
###>>> test = "have it break."
###>>> selectiveEscape = "Print percent %% in sentence and not %s" % test
###>>> print selectiveEscape
###Print percent % in sentence and not have it break

###>>> print "We have %d pallets of %s today." % (49, "kiwis")
###We have 49 pallets of kiwis today.

                            with open("MokkaSteering.steer" ,"w") as SteeringFile:
                                SteeringFile.write( getMokkaSteeringFileTemplate(self._GeometryAdaption,
                                                                                 PhysicsList = self._PhysicsList,
                                                                                 HCalAbsorberMaterial = self._HCalAbsorberMaterial,
                                                                                 HCalAbsorberLayerThickness = self._HCalAbsorberLayerThickness,
                                                                                 HCalScintillatorThickness = self._HCalScintillatorThickness,
                                                                                 CoilExtraSize = self._CoilExtraSize,
                                                                                 DetailedShowerMode = self._DetailedShowerMode,
                                                                                 Identifier = self._Identifier,
                                                                                 NumberHCalLayers = self._NumberHCalLayers,
                                                                                 BField = self._BField,
                                                                                 TPCOuterRadius = self._TPCOuterRadius,
                                                                                 HCalCellSize = self._HCalCellSize,
                                                                                 DetectorModel = self._DetectorModel,
                                                                                 OutputFilename = MyOutputFilename,
                                                                                 GearFilename = MyGearOutputFilename))

                            job = UserJob()
                            MokkaApplication = Mokka()
                            MokkaApplication.setVersion( self._MokkaVersion )
                            MokkaApplication.setSteeringFile( "MokkaSteering.steer" )
                            MokkaApplication.setNumberOfEvents( EventsPerJob )
                            MokkaApplication.setStartFrom( StartEvent )
                            job.setJobGroup( self._JobIdentificationString )
                            job.setOutputSandbox( ["*.log", "*.gear", "*.mac", "*.steer", "*.xml" ] )
                            job.setOutputData( MyOutputFilename, OutputPath=MyOutputPath )
                            job.setInputData( FileLFN )
                            job.setName(MyOutputFilename)
                            job.setBannedSites(['LCG.IN2P3-CC.fr','LCG.IN2P3-IRES.fr'])
                            # Debug Issue
                            #job.setLogLevel("DEBUG")
                            
                            res = job.append(MokkaApplication)
                            if not res['OK']:
                                gLogger.error("JobSumit Error:", res["Message"] )
                                raise Exception( "MyError: ", res["Message"] )
                            else:
                                pass
                            if not self._dryRun:
                                job.submit(self._DiracInstance)
                                #job.submit(DiracInstance,mode="local")
                        else:
                            JobCounter -= 1
                            #finish jobs loop
        print "\nWe created %d jobs!" % ( JobCounter+1 )
### ----------------------------------------------------------------------------------------------------
### End of submitJobs
### ----------------------------------------------------------------------------------------------------
### Start of getAFiles
### ----------------------------------------------------------------------------------------------------

def getAFiles(EventType, Energy, no):
    list = getListOfFiles(EventType, Energy)
    
    if no!=-1:
        print [list[no]]
        return [list[no]]
    else:
        return list

### ----------------------------------------------------------------------------------------------------
### End of getAFiles
### ----------------------------------------------------------------------------------------------------
### Start of getListOfFiles
### ----------------------------------------------------------------------------------------------------

def getListOfFiles(EventType, Energy):
    if EventType == "Z_uds":
        if Energy == 91:
            list=[ {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/00.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/01.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/02.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/03.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/04.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/05.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/06.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/07.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/08.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/91gev/Z_uds/gen/0/09.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"}]
        elif Energy == 200:
            list=[ {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/00.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/01.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/02.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/03.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/04.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/05.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/06.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/07.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/08.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/200gev/Z_uds/gen/0/09.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"}]
        elif Energy == 360:
            list=[ {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_00.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_01.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_02.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_03.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_04.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_05.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_06.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_07.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_08.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/360gev/Z_uds/gen/0/uds360_09.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"}]
        elif Energy == 500:
            list=[ {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/00.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/01.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/02.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/03.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/04.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/05.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/06.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/07.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/08.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/500gev/Z_uds/gen/0/09.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"}]
        elif Energy == 750:
            list=[ {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_00.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_01.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_02.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_03.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_04.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_05.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_06.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_07.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_08.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/750gev/Z_uds/gen/0/uds750_09.stdhep", 'nEvents': 1000, 'eventType': "Z_uds"}]
        elif Energy == 1000:
            list=[ {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_00.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_01.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_02.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_03.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_04.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_05.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_06.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_07.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_08.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_09.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_10.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_11.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_12.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_13.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_14.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_15.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_16.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_17.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_18.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_19.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_20.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_21.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_22.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_23.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_24.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_25.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_26.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_27.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_28.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_29.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_30.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_31.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_32.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_33.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_34.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_35.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_36.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_37.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_38.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_39.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_40.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_41.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_42.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_43.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_44.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_45.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_46.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_47.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_48.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_49.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_50.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_51.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_52.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_53.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_54.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_55.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_56.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_57.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_58.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_59.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_60.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_61.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_62.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_63.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_64.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_65.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_66.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_67.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_68.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_69.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_70.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_71.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_72.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_73.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_74.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_75.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_76.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_77.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_78.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_79.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_90.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_91.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_92.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_93.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_94.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_95.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_96.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_97.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_98.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_99.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_90.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_91.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_92.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_93.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_94.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_95.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_96.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_97.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_98.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/1000gev/Z_uds/gen/0/uds1000_99.stdhep", 'nEvents': 100, 'eventType': "Z_uds"}]
        elif Energy == 2000:
            list=[ {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_00.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_01.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_02.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_03.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_04.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_05.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_06.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_07.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_08.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_09.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_10.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_11.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_12.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_13.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_14.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_15.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_16.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_17.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_18.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_19.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_20.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_21.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_22.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_23.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_24.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_25.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_26.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_27.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_28.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_29.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_30.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_31.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_32.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_33.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_34.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_35.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_36.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_37.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_38.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_39.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_40.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_41.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_42.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_43.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_44.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_45.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_46.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_47.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_48.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_49.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_50.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_51.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_52.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_53.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_54.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_55.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_56.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_57.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_58.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_59.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_60.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_61.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_62.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_63.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_64.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_65.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_66.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_67.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_68.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_69.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_70.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_71.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_72.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_73.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_74.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_75.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_76.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_77.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_78.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_79.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_80.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_81.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_82.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_83.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_84.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_85.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_86.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_87.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_88.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_89.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_90.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_91.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_92.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_93.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_94.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_95.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_96.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_97.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_98.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/2000gev/Z_uds/gen/0/uds2000_99.stdhep", 'nEvents': 100, 'eventType': "Z_uds"}]
        elif Energy == 3000:
            list=[ {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_00.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_01.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_02.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_03.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_04.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_05.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_06.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_07.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_08.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_09.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_10.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_11.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_12.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_13.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_14.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_15.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_16.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_17.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_18.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_19.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_20.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_21.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_22.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_23.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_24.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_25.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_26.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_27.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_28.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_29.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_30.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_31.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_32.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_33.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_34.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_35.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_36.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_37.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_38.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_39.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_40.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_41.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_42.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_43.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_44.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_45.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_46.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_47.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_48.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_49.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_50.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_51.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_52.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_53.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_54.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_55.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_56.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_57.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_58.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_59.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_60.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_61.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_62.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_63.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_64.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_65.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_66.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_67.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_68.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_69.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_70.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_71.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_72.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_73.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_74.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_75.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_76.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_77.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_78.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_79.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_80.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_81.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_82.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_83.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_84.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_85.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_86.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_87.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_88.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_89.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_90.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_91.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_92.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_93.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_94.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_95.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_96.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_97.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_98.stdhep", 'nEvents': 100, 'eventType': "Z_uds"},
                   {'name':"/ilc/prod/clic/3000gev/Z_uds/gen/0/uds3000_99.stdhep", 'nEvents': 100, 'eventType': "Z_uds"}]
        else:
            raise Exception("No Z->UDS Events for this energy %d" % (Energy) )

    elif EventType == "Muon":
        if Energy == 1:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Muon/1GeV/Muon_1GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000} ]
        elif Energy == 5:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Muon/5GeV/Muon_5GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000} ]
        elif Energy == 10:
            list=[ {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Muon/10_GeV_Energy_13_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 20:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Muon/20GeV/Muon_20GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000} ]
        elif Energy == 30:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Muon/30GeV/Muon_30GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000} ]
        elif Energy == 40:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Muon/40GeV/Muon_40GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000} ]
        elif Energy == 50:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Muon/50GeV/Muon_50GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Muon", 'MaxNumberOfEvents': 1000} ]
        else:
            raise Exception("No Muon Events for this energy %d" % (Energy) )

    elif EventType == "Kaon0L":
        if Energy == 1:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/1_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 2:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/2_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 3:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/3_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 4:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/4_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 5:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/5_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 6:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/6_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 7:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/7_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 8:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/8_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 9:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/9_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 10:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/10_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 15:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/15_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 20:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/20_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 25:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/25_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 30:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/30_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 35:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/35_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 40:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/40_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 45:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/45_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 50:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/50_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 100:
            list=[  {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000},
                    {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/KaonL/100_GeV_Energy_130_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Kaon0L", 'MaxNumberOfEvents': 1000}
                 ]
        else:
            raise Exception("No Kaon0L Events for this energy %d" % (Energy) )

    elif EventType == "Photon":
        if Energy == 1:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/1GeV/Photon_1GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Photon"} ]
            #list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/1GeV/Photon_1GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 100, 'eventType': "Photon"} ]
        elif Energy == 5:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/5GeV/Photon_5GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Photon"} ]
        elif Energy == 10:
            list=[ {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_1.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_2.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_3.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_4.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_5.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_6.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_7.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_8.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_9.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000},
                   {'name':"/ilc/user/s/sgreen/HEPEvt/SingleParticles/Photon/10_GeV_Energy_22_pdg_SN_10.HEPEvt", 'nEvents': 1000, 'eventType': "Photon", 'MaxNumberOfEvents': 1000}
                 ]
        elif Energy == 20:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/20GeV/Photon_20GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Photon"} ]
        elif Energy == 30:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/30GeV/Photon_30GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Photon"} ]
        elif Energy == 40:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/40GeV/Photon_40GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Photon"} ]
        elif Energy == 50:
            list=[ {'name':"/ilc/prod/clic/SingleParticles/Photon/50GeV/Photon_50GeV_Fixed_cosTheta0.7.stdhep", 'nEvents': 10000, 'eventType': "Photon"} ]
        else:
            raise Exception("No Photon Events for this energy %d" % (Energy) )

    elif EventType == "Tau":
        if Energy == 100:
            list=[ {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.000.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.001.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.002.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.003.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.004.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.005.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.006.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.007.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.008.stdhep", 'nEvents': 100001, 'eventType': "Tau"},
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots100.009.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ]
        elif Energy == 500:
            list=[ {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.000.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.001.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,     
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.002.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.003.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.004.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.005.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.006.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.007.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.008.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,            
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots500.009.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ]
        elif Energy == 1000:
            list=[ {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.000.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.001.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.002.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.003.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.004.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.005.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.006.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.007.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.008.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots1000.009.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ]
        elif Energy == 200:
            list=[ {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.000.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.001.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.002.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.003.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.004.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.005.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.006.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.007.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.008.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ,
            {'name':"/ilc/user/a/alucacit/ECAL/stdhep/whizard.ee_tautau_roots200.009.stdhep", 'nEvents': 100001, 'eventType': "Tau"} ]
        else:
            raise Exception("No Photon Events for this energy %d" % (Energy) )

    else:
        raise Exception("Unknown Eventtype %s" % (EventType) )

    return list

### ----------------------------------------------------------------------------------------------------
### End of getListOfFiles
### ----------------------------------------------------------------------------------------------------
### Start of getMokkaSteeringFileTemplate function
###
### Basis for the steering file, macroname must not be specified as it will be
### created by dirac based on the input file and the number of events
### ----------------------------------------------------------------------------------------------------

def getMokkaSteeringFileTemplate(GeometryAdaption, 
                              PhysicsList="QGSP_BERT",
                              HCalAbsorberMaterial="Iron",
                              HCalAbsorberLayerThickness="20.0",
                              HCalScintillatorThickness="3.0",
                              CoilExtraSize=1522,
                              DetailedShowerMode="false",
                              Identifier="Dummy",
                              NumberHCalLayers=48,
                              BField=3.5,
                              TPCOuterRadius=1808,
                              HCalCellSize=30,
                              OutputFilename="Output.slcio", 
                              GearFilename="GearFile.gear",
                              StartEventNumber=0,
                              DetectorModel="",
                              RangeCut="0.05 mm"):
    
    MokkaSteeringFile="""
/Mokka/init/userInitString TIMEOUT_TO_RELAX_TMP 120
/Mokka/init/userInitInt SLEEP_BEFORE_RETRY 5
/Mokka/init/randomSeed 782354721
/Mokka/init/startEventNumber """, StartEventNumber,"""
/Mokka/init/detectorModel """, DetectorModel,"""
/Mokka/init/physicsListName """, PhysicsList,"""
/Mokka/init/rangeCut """, RangeCut, """
/Mokka/init/savingTrajectories false
/Mokka/init/savingPrimaries false
/Mokka/init/lcioWriteMode WRITE_NEW
/Mokka/init/lcioStoreCalHitPosition true
/Mokka/init/MokkaGearFileName """, GearFilename, """

/Mokka/init/EditGeometry/rmSubDetector SServices00

/Mokka/init/globalModelParameter Ecal_Sc_Si_mix 000000000000000
/Mokka/init/globalModelParameter Ecal_Sc_number_of_virtual_cells 1
/Mokka/init/globalModelParameter Ecal_cells_size 5.0
/Mokka/init/globalModelParameter Ecal_Sc_N_strips_across_module 36
/Mokka/init/globalModelParameter Ecal_MPPC_size 0.91
/Mokka/init/globalModelParameter Ecal_guard_ring_size 0.00001
/Mokka/init/globalModelParameter Ecal_nlayers1 20
/Mokka/init/globalModelParameter Ecal_nlayers2 9
/Mokka/init/globalModelParameter Ecal_nlayers3 0
/Mokka/init/globalModelParameter Ecal_radiator_layers_set1_thickness 2.1
/Mokka/init/globalModelParameter Ecal_radiator_layers_set2_thickness 4.2
/Mokka/init/globalModelParameter Ecal_radiator_layers_set3_thickness 0
/Mokka/init/globalModelParameter Ecal_Si_thickness 0.5
/Mokka/init/globalModelParameter Ecal_Sc_thickness 2.0
/Mokka/init/globalModelParameter Ecal_Slab_Sc_PCB_thickness 0.9
/Mokka/init/globalModelParameter Hcal_Ecal_gap 30.0
/Mokka/init/globalModelParameter Hcal_endcap_ecal_gap 15.0

/Mokka/init/globalModelParameter Hcal_radiator_material """, HCalAbsorberMaterial, """
/Mokka/init/globalModelParameter Hcal_endcap_radiator_material """, HCalAbsorberMaterial, """

/Mokka/init/globalModelParameter Hcal_cells_size """, HCalCellSize, """

/Mokka/init/globalModelParameter Hcal_radiator_thickness """, HCalAbsorberLayerThickness, """
/Mokka/init/globalModelParameter Hcal_endcap_radiator_thickness """, HCalAbsorberLayerThickness, """

/Mokka/init/globalModelParameter Hcal_scintillator_thickness """, HCalScintillatorThickness, """

/Mokka/init/globalModelParameter Hcal_nlayers """, NumberHCalLayers, """
/Mokka/init/globalModelParameter Hcal_endcap_nlayers """, NumberHCalLayers, """

/Mokka/init/globalModelParameter Field_nominal_value """, BField, """
/Mokka/init/globalModelParameter TPC_outer_radius """, TPCOuterRadius, """

/Mokka/init/globalModelParameter Yoke_Z_start_endcaps 4072
/Mokka/init/globalModelParameter Coil_Yoke_lateral_clearance 200
/Mokka/init/globalModelParameter Coil_extra_size """, CoilExtraSize, """

/Mokka/init/lcioDetailedShowerMode """, DetailedShowerMode, """

/Mokka/init/BatchMode true
/Mokka/init/lcioFilename """, OutputFilename, """
/Mokka/init/initialMacroFile $workDir/$2_$3_SiW.g4macro

### User Provided Geometry
"""
    MokkaSteeringFile = "".join(map(str, MokkaSteeringFile))
    MokkaSteeringFile += GeometryAdaption

    return MokkaSteeringFile
### ----------------------------------------------------------------------------------------------------
### End of getMokkaSteeringFileTemplate function
### ----------------------------------------------------------------------------------------------------
