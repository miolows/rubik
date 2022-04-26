from direct.showbase.ShowBase import ShowBase
from panda3d.core import LVecBase4f, loadPrcFileData
# from direct.task import Task

from bin.calculations.cube.rubik import Rubik
from bin.calculations.calc_visu_comm import CalcVisuCommunication

from bin.visualisation.events.ievent import event_sender
from bin.visualisation.events.camera_event import CameraHandler
from bin.visualisation.events.animation_event import RubikAnimationHandler

from bin.visualisation.visu_calc_comm import VisuCalcCommunication
from bin.visualisation.vrubik import VRubik 


confVars = """
show-frame-rate-meter 1
show-scene-graph-analyzer-meter 1

"""

loadPrcFileData("", confVars)


class App(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        self.shape = (3,3,3)
        self.qb_len = 1.5
        
        
        self.colors = {
            0: LVecBase4f(0.0, 0.0, 0.0, 1.0), # Black
            1: LVecBase4f(0.0, 1.0, 0.0, 1.0), # Green                              
            2: LVecBase4f(0.0, 0.0, 1.0, 1.0), # Blue
            3: LVecBase4f(1.0, 0.0, 0.0, 1.0), # Red 
            4: LVecBase4f(1.0, 0.5, 0.0, 1.0), # Orange                             
            5: LVecBase4f(1.0, 1.0, 0.0, 1.0), # Yellow
            6: LVecBase4f(1.0, 1.0, 1.0, 1.0)  # White
        }
        
        
        rubik = Rubik(self.shape)
        rubik_data = rubik.get_rubik_data()

        
        #rc = RubiksCube(shape = shape)

        vrubik = VRubik(self.shape, rubik_data, self.qb_len, self.colors, self.taskMgr)
        rah = RubikAnimationHandler(vrubik.rubik_node)
        vc_mediator = VisuCalcCommunication()
        
        cv_mediator = CalcVisuCommunication(rubik, vc_mediator)
        # 
        # RubikCalculationHandler(rc)
        # RubikCommunicationHandler()
        
                               
        


        self.disableMouse()
        
        environ = self.loader.loadModel('environment')
        environ.setScale(0.1)
        environ.setZ(-10)
        environ.reparentTo(self.render)


        self.camera_handler = CameraHandler(vrubik.rubik_node)
        self.accept("mouse3", event_sender, ['Camera Rotation Start'])
        self.accept("mouse3-up", event_sender, ['Camera Rotation Stop'])
        self.accept('wheel_up', event_sender, ['Camera Zoom In'])        
        self.accept('wheel_down', event_sender, ['Camera Zoom Out'])
        
        
        self.accept("q", event_sender, ['Rubik Rotation', 0, 0, 1])
        self.accept("w", event_sender, ['Rubik Rotation', 1, 0, 1])
        self.accept("e", event_sender, ['Rubik Rotation', 2, 0, 1])
        self.accept("0", event_sender, ['Rubik Mix', 30])
        # b = DirectButton(text=("OK", "click!", "rolling over", "disabled"))
    