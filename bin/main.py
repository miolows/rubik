# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 14:48:54 2020

@author: olows
"""
from bin.visualisation.visualisation import App


# shape = (3,3,3)
# qb_len = 1.5


# colors_pallet = [LVecBase4f(0.0, 0.0, 0.0, 1.0), # Black
#                 LVecBase4f(0.0, 1.0, 0.0, 1.0), # Green                              
#                 LVecBase4f(0.0, 0.0, 1.0, 1.0), # Blue
#                 LVecBase4f(1.0, 0.0, 0.0, 1.0), # Red 
#                 LVecBase4f(1.0, 0.5, 0.0, 1.0), # Orange                             
#                 LVecBase4f(1.0, 1.0, 0.0, 1.0), # Yellow
#                 LVecBase4f(1.0, 1.0, 1.0, 1.0)] # White

# rc = RubiksCube(shape = shape)
# cube1 = rc.GetCube()
# vrc = VRubik(shape, cube1, qb_len, colors_pallet, base.taskMgr)
# mediator = StefanMediator(rc, vrc, base.taskMgr)



if __name__ == "__main__":
    
    a = App()
    a.run()
    # a.run()
    # rc = RubiksCube()
    # ax_lay = (0,0)
    # # print(rc.GetLayer(*ax_lay))
    # rc.Rotate(*ax_lay, 1)
    # # print(rc.GetLayer(*ax_lay))
    