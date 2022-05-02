from direct.showbase.DirectObject import DirectObject
# from panda3d.core import *

from bin.visualisation.events.ievent import *
import numpy as np


class CameraHandler(IEventOrganiser):
    def __init__(self, anchor):
        super().__init__()
        self.camera_anchor = anchor
        self.cam = base.cam
        self.camera = base.camera
        self.camera.reparentTo(self.camera_anchor)
        self.camera_holder = self.camera_anchor.attachNewNode("Camera Holder")
        self.taskMgr = base.taskMgr
        
        #Rotation variables
        self.camera_rotation_task_name = "Camera Rotation"
        self.camera_rotation_speed = 150
        self.mouse_start_pos = (0,0,0)
        self.mouse_watcher_node = base.mouseWatcherNode
        
        #Zoom variables
        self.cam_zoom_max_in = -5
        self.cam_zoom_max_out = -30
        self.cam_zoom_speed = 30
        self.cam_zoom_step = 3
        self.cam_zoom_pos = -10
        
        #Camera POV variables
        self.pov_border = tuple(self.camera.getHpr())
        self.cam_switch = 45
        
        self.cam.setY(self.cam_zoom_pos)


    @handle_event('Camera Rotation Start')
    def camera_rotation_start(self):
        start_x = self.mouse_watcher_node.getMouseX()
        start_y = self.mouse_watcher_node.getMouseY()
        self.mouse_start_pos = (start_x, start_y)
        self.taskMgr.add(self.camera_rotation_task, 
                         self.camera_rotation_task_name)
        

        
    @handle_event('Camera Rotation Stop')        
    def camera_rotation_stop(self):
        self.taskMgr.remove(self.camera_rotation_task_name)
        # self.camera.wrtReparentTo(self.camera_anchor)
    
    
    @handle_event('Camera Zoom In')
    def zoom_in(self):
        self.wheel(1)
        
    @handle_event('Camera Zoom Out')
    def zoom_out(self):
        self.wheel(-1)
    
    
    def camera_rotation_task(self, task):
        '''
        It only works when the mouse cursor is in the program window. 
        
        Adjusts the camera holder to the camera position, attaches the dummy to 
        it and the camera to the dummy, keeping the previous position. The dummy 
        has its own direction of rotation and is independent of the parent, 
        so that the mouse movement always rotates the camera in the same direction 
        (from the user's point of view).                                   
        
        |Note:
        ||This algorithm mimics a default camera rotation control. 
        ||The disadvantage is that if there is a need to add another camera
        ||event that needs to be independent of the actual camera position in 
        ||the Scene Graph, an additional handle node is needed, bBut it can 
        ||also break other event handlers.
        '''
        if self.mouse_watcher_node.hasMouse():
            
            self.camera_holder.setHpr(self.camera.getHpr())
            camera_rotation_node = self.camera_holder.attachNewNode("Camera Rotation Node")
            self.camera.wrtReparentTo(camera_rotation_node)
            
            start_x, start_y = self.mouse_start_pos
            x = self.mouse_watcher_node.getMouseX()
            y = self.mouse_watcher_node.getMouseY()
            delta_x = start_x - x
            delta_y = y - start_y
            
            heading = delta_x * self.camera_rotation_speed
            pitch = delta_y * self.camera_rotation_speed
            
            camera_rotation_node.setHpr(heading, pitch, 0.0 )
            self.mouse_start_pos = (x,y)
            self.camera.wrtReparentTo(self.camera_anchor)
            camera_rotation_node.removeNode()
            # self.camera_pov()
        return task.cont
    
    ''' A struggle to code a camera point of view. In vain, mostly because: 
        1. it doesn't work properly in the panda module,
        2. it has some problems with turning camera near axis,
        3. it generates too many spread changes,
        4. can generate further issues with an ambiguity between calc and visu modules.
    '''
    # def camera_pov(self):
    #     new_camera_pos = tuple(self.camera.getHpr())
    #     delta = np.subtract(new_camera_pos, self.pov_border)
    #     check_flip = delta / self.cam_switch
    #     check_flip = [int(x) for x in check_flip]
    #     no_flip = all(hpr == 0 for hpr in check_flip)
    #     if no_flip:
    #         pass
    #     else:
    #         camera_flip = tuple(np.multiply(90,check_flip))
    #         camera_flip = tuple(np.add(self.pov_border, camera_flip))
    #         self.pov_border= camera_flip
    #         messenger.send("Camera POV", check_flip)
            
    def wheel(self, direction:int):
        '''
        Performs camera zoom events.
        Parameters
        ----------
        direction : int - Zooming direction (1 - zoom in; -1 - zoom out)
        
        |Notes:
        ||Occasionally, the camera may jitter when a user is spamming the scroll 
        ||wheel. It's not a big problem, but looks rather bad and should to be 
        ||fixed. It can be fun to add some smart event to set the zoom limits, 
        ||depending on the contents of the Scene Graph.
        '''
        self.cam_zoom_pos += direction * self.cam_zoom_step
        
        #check of zooming borders
        if self.cam_zoom_pos > self.cam_zoom_max_in:
            self.cam_zoom_pos = self.cam_zoom_max_in
        elif self.cam_zoom_pos < self.cam_zoom_max_out:
            self.cam_zoom_pos = self.cam_zoom_max_out
    
        curr_pos = self.cam.getY()        
        zoom_shift = abs(self.cam_zoom_pos - curr_pos)
        zoom_time = zoom_shift/self.cam_zoom_speed
        
        Sequence(self.cam.posInterval(zoom_time, 
                                      (0, self.cam_zoom_pos, 0)
                                      )).start()