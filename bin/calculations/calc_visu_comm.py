from abc import ABC
import queue
import numpy as np

from bin.calculations.cube.rubik_plot import RubikHistory


class Mediator(ABC):

    def notify(self, event: str, *more_events) -> None:
        pass


class CVCommComponent:
    """
    The CVBaseComponent provides the basic functionality for storing a mediator 
    instance inside its component objects.
    """

    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator
        


class CalcVisuCommunication(Mediator):
    ''' Calc -> Visu'''
    ''' Mediator between calculations and visualisation modules '''
    ''' This class has direct access to rubik and mediator on visualisation site '''   
    def __init__(self, calc_instance, visu_instance) -> None:
        self.calc = calc_instance
        self.calc.mediator = self
        self.visu = visu_instance
        self.visu.mediator = self
        
        self.ambiguity = False      #A flag indicating discrepancy between the modules
        #self.calc_plot = RubikHistory(6)

    def notify(self, event: str, *data) -> None:
        events = {
                'Rubik Rotation':           self.calc_rotation,
                'Rubik Blind Rotation':     self.calc_blind_rotation,
                'Rubik Mix':                self.calc_mix,
                'Rubik Blind Mix':          self.calc_blind_mix,
                'Rubik Reset':              self.calc_reset,
                # 'Camera POV':               self.camera_pov,
                
                'Rotation Response':        self.visu_rotation,
                'Mix Response':             self.visu_mix,
                'Reset Response':           self.visu_reset,                
                }
        events[event](*data)
        
    def calc_rotation(self, *data):
        # self.calc.rotate(*data)
        # self.calc.print_faces_interpret(self.calc.colors)
        axis, layer_n, _ = data
        position = self.calc.get_layer_pos(self.calc.layers(axis)[layer_n])
        response = (data, position)
        self.notify('Rotation Response', *response)
       # self.plot_value()
        
        
    def calc_blind_rotation(self, *data):
        pass
        
        
    def calc_mix(self, *data):
        n = data[0]
        response = []
        for i in range(n):
            rot_data = self.calc.rand_rotate()
            axis, layer, _ = rot_data
            
            position = self.calc.get_layer_pos(self.calc.layers(axis)[layer])
            out = (rot_data, position)
            response.append(out)
        self.notify('Mix Response', response)
        
        
    def calc_blind_mix(self, *data):
        pass
    def calc_reset(self, *data):
        pass
    
    # def camera_pov(self, *data):
    #     h_num, p_num, r_num = np.absolute(data) #number of flips
    #     h_dir, p_dir, r_dir = np.sign(data) #direcktion of flips
                
    #     for x in range(p_num):
    #         self.calc.flip(0, -p_dir)
            
    #     for y in range(r_num):
    #         self.calc.flip(1, -r_dir)
            
    #     for z in range(h_num):
    #         self.calc.flip(2, -h_dir) 
        
    
    
    def visu_rotation(self, *data):
        self.visu.rotation_response(*data)    
        
    def visu_mix(self, *data):
        self.visu.mix_response(*data) 
        pass
    def visu_reset(self, *data):
        pass

'''
    def plot_value(self):
        val = self.calc.rubik_val
        shape = self.calc.shape
        faces = []
        for ax in range(len(shape)):
            layers = list(map(lambda x: np.squeeze(x), np.split(val, np.arange(1, shape[ax]),axis=ax)))
            faces.append(np.sum(layers[0]))
            faces.append(np.sum(layers[-1]))
        
        self.calc_plot.add_data(faces)
        self.calc_plot.plot()
'''
