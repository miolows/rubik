from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *
from panda3d.core import *

from bin.visualisation.events.ievent import *
from bin.calculations.calc_visu_comm import CVCommComponent

class VisuCalcCommunication(CVCommComponent, IEventOrganiser):
    ''' Visu -> Calc '''
    ''' Mediator-like class between calculations and visualisation modules '''
    ''' This class has direct access to rubik and mediator on visualisation site '''
    def __init__(self):
        CVCommComponent.__init__(self)
        IEventOrganiser.__init__(self)
        self.rotation_anim_speed = 180.0
        self.mix_anim_speed = 10000.0
        self.anim_speed = self.rotation_anim_speed
 
    
    ''' Visu -> Calc: Invoke various actions in the calculations module '''
    @handle_event('Rubik Rotation')
    def calc_rotation(self, *data):
        self.anim_speed = self.rotation_anim_speed
        response = self.mediator.notify('Rubik Rotation', *data)
        # print(response)
        # translated_response = self.translate_command(*response)
        # event_sender("Animation Of Rubik Rotation", *translated_response)
        
    @handle_event('Rubik Mix')
    def send_mix_calc_event(self, num=30):
        self.anim_speed = self.mix_anim_speed
        self.mediator.notify('Rubik Mix', num)
        
       
        
    ''' Calc -> Visu: Handle responses of the calculations module '''
    def rotation_response(self, *response):
        translated_response = self.translate_command(*response)
        event_sender("Animation Of Rubik Rotation", *translated_response)
               
    def mix_response(self, *response):
        mix_list = response[0]
        for mix in mix_list:
            translated_response = self.translate_command(*mix)
            event_sender("Animation Of Rubik Rotation", *translated_response)
        
        
        
    def translate_command(self, *args):
        ''' Helper method '''
        rot_args, positions = args
        axis, layer, direction = rot_args
        rotation = [0,0,0]
        angle = 90.0 * direction
        
        rotation[axis] = angle
        # HPR corresponds to rotation around z, x and y axis
        pitch, roll, heading = rotation
        
        time = abs(angle / self.anim_speed)
        hpr = (heading, pitch, roll)
        
        return (time, hpr, positions)
    
    