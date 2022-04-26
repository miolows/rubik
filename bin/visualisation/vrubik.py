# from panda3d.core import *
from panda3d.core import Geom, GeomNode, GeomVertexData, GeomVertexFormat, GeomVertexWriter, GeomTristrips
import numpy as np


class VQb(Geom):
    def __init__(self, cube, colors_pallet):
        self.cube = cube
        self.colors = colors_pallet
        
        self.geom_format = GeomVertexFormat.get_v3cp()
        self.geom_uhs = Geom.UHStatic
        self.geom_data = GeomVertexData("Qubie", self.geom_format, self.geom_uhs)
        
        self.geom_data.setNumRows(24)
        
        self.vertexWriter = GeomVertexWriter(self.geom_data,"vertex")
        self.colorWriter = GeomVertexWriter(self.geom_data, "color")
        super().__init__(self.geom_data)        
        
        
        self.vertex_index = 0
        
        for coord, color in np.ndenumerate(self.cube):
            self.add_face(coord, color)       
            
        
    def add_face(self, coords, color):
        face = GeomTristrips(self.geom_uhs)
        vers = [[0,0], [0,1], [1,0], [1,1]] # Vertices of 2D square
        for v in vers:
            v = v.insert(coords[0],coords[1]) #Set face in 3 dim, depending on location in Cubie
        
        face_vert = list(map(tuple, vers))
        face_color = color
        for crd in face_vert:
            self.vertexWriter.addData3f(crd)
            self.colorWriter.addData4(self.set_color(face_color))
            face.addVertex(self.vertex_index)
            self.vertex_index+=1
        face.closePrimitive()
        self.addPrimitive(face)
        
    def set_color(self, index):
        return self.colors[index]
    


class VRubik():
    def __init__(self, shape, cube, qb_len, colors_pallet, task_manager):
        self.shape = shape
        self.cube = cube
        self.len = qb_len
        self.colors = colors_pallet
        self.task_mgr = task_manager
        
        self.gap = 0.01 * self.len
        
        self.rubik_node = render.attachNewNode("Rubik")        
        # self.dynamic_node = self.rubik.attachNewNode("Dynamic Node")      # parent of moving cubies
        self.static_node = self.rubik_node.attachNewNode("Static Node")        # parent of non-moving cubies
        
        self.initCube()

#~~~ Functions used to create, paint and position model ~~~#
    def initCube(self):
        self.drawCubies(self.cube)

    def drawCubies(self, cubies):
        for c in cubies:
            qb_index = c[0]
            qb_data = c[1]
            
            qubie_geom = VQb(qb_data, self.colors)
            qubie_node = GeomNode("{}".format(qb_index))  
            qubie_node.addGeom(qubie_geom)
            qb_node_path = self.static_node.attachNewNode(qubie_node)
            qb_node_path.setTwoSided(True)
            # Scale cubies
            qb_node_path.setScale(self.len)
            # Arange whole Cube
            newPos = tuple(map(lambda x,y: x-y, self.calcPos(qb_index), self.calcCenter()))
            qb_node_path.setPos(newPos)
        

    def calcPos(self, coord):
        return tuple(map(lambda x: np.multiply(x, self.len+self.gap), coord))


    def calcCenter(self):
        #Lenght of each side
        side_len = list(map(lambda x: np.multiply(x, self.len) + np.multiply(x-1, self.gap),self.shape))
        #tuple of centers of each side
        return tuple(map(lambda x: np.multiply(x, 0.5), side_len))

if __name__ == '__main__':
    pass