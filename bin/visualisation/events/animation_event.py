from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence, Func
from panda3d.core import NodePathCollection
import queue

from bin.visualisation.events.ievent import *


class RubikAnimationHandler(IEventOrganiser):
    def __init__(self, rubik_node_path):
        super().__init__()
        self._rubik_node_path = rubik_node_path
        self._holder_node_path = self._rubik_node_path.getChild(0)    #assuming rubik has only one child
        self._rotation_tasks_queue = queue.Queue()
        self._rotation_task_name = "Rotate"
        self._rotation_time = 0.5   # [sec]
        self._task_proceed = False

                
    @handle_event('Animation Of Rubik Rotation')
    def arrange_rotation_event(self, *data):
        
        if self._task_proceed is False:
            self.rotate_rubik(*data)
        else:
            self._rotation_tasks_queue.put(data)
    
    
    def invoke_next_event(self):
        self._task_proceed = False
        if self._rotation_tasks_queue.empty() is not True:
            next_event = self._rotation_tasks_queue.get()
            self.rotate_rubik(*next_event)
    
    
    def rotate_rubik(self, *data):
        self._task_proceed = True
        time, hpr, positions = data     
        rotation_node = self._rubik_node_path.attachNewNode("Dynamic Node")
        collection = NodePathCollection()
        for pos in positions:
            path = self._rubik_node_path.find('**/{}'.format(pos))
            
            collection.addPath(path)
            
        preparations = Func(self.reparent, collection, rotation_node)
        rotation_interval = rotation_node.hprInterval(time, hpr)
        finishing_touches = Func(self.update, collection, rotation_node)
        next_event = Func(self.invoke_next_event)
        
        Sequence(preparations, 
                 rotation_interval, 
                 finishing_touches, 
                 next_event).start()
    
    
    def reparent(self, reparent_what, reparent_to):
        for node in reparent_what:
                node.reparentTo(reparent_to)
                
    def update(self, reparent_what, holder_node):
        for node in reparent_what:
            node.wrtReparentTo(self._holder_node_path)
           
        holder_node.removeNode()
               
