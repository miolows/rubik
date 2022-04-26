import numpy as np
import random
from collections import Counter
import functools
from bitarray import bitarray
from bitarray.util import ba2int

from bin.calculations.calc_visu_comm import CVCommComponent
from bin.calculations.cube.qb import Qb
from bin.calculations.cube.wrapper import timer

class Rubik(CVCommComponent):
    def __init__(self, s=(3,3,3)):
        CVCommComponent.__init__(self)
        self._shape = s
        self.rubik = np.ndarray((self.shape),dtype="object") #'''<- 18.03 dodano dtype'''
        self.no_val = 0 # A value of hidden faces, without any meaning. If present on the outer layer, this is an error.
        self.values = list(range(self.no_val+1, (self.num_axis * self.num_sides)+1))
        
        
        '''18.03 ->'''
        self.rubik = np.array([Qb(i) for i,x in np.ndenumerate(self.rubik)]).reshape(self.shape)
        #array is flatten to map it and fill with the default instances of small cubes (Qb)
        #self.rubik = np.array(list(map(lambda x: Qb(), self.rubik.flatten()))).reshape(self.shape)
        '''<- 18.03'''

        self.set_rubik()
        self.max_solved, self.rubik_max_val = self.calc_rubik_value()
        self.how_solved, self.rubik_val = self.max_solved, self.rubik_max_val


    ''' ***************** immutable properties ***************** '''

    @property
    def shape(self):
        """Get value of a shape. An immutable property."""
        return self._shape
    
    @property
    def sides(self):
        """Get an array of the sides of an array (i.e. the first and the last side). An immutable property."""
        return [0,-1]
    
    @property
    def num_axis(self):
        """Get a number of dimentions (axies) of a rubik. An immutable property."""
        return len(self.shape)
    
    @property
    def num_sides(self):
        """Get a number of sides. An immutable property."""
        return len(self.sides)

    ''' ****************************************************************** '''
    ''' ***************** setter and getter ***************** '''
    
    def set_rubik(self):
            num_faces = self.num_axis * self.num_sides
            values = list(range(0, num_faces+1))
            v=0
            for ax in range(self.num_axis):
                rubik_layers = self.layers(ax)
                for side in self.sides:
                    layer = rubik_layers[side]
                    
                    # this single line sets values (colors) not only in 
                    # the local array (cube_layer), but also in original 
                    # (self.rubik) and I don't know why...
                    # But that's actually what I wanted to do anyway
                    list(map(lambda x: x.set_qb(self.values[v], ax, side), layer.flatten()))
                    v+=1


    def get_rubik(self):
        return np.array(list(map(lambda x: x.get_qb(), self.rubik.flatten())))
    
    '''18.03 ->'''  
    def get_layer_data(self, layer):
        data = [(c.get_position(), c.get_qb_data()) for _, c in np.ndenumerate(layer)]
        return data
    
    def get_layer_pos(self, layer):
        data = [c.get_position() for _, c in np.ndenumerate(layer)]
        return data
    
    def get_rubik_data(self):
        data = [(c.get_position(), c.get_qb_data()) for _, c in np.ndenumerate(self.rubik)]
        return data
    
    # def get_rubik_data(self):
    #     data = []
    #     for index, c in np.ndenumerate(self.rubik):
    #         qb_data = (index, c.get_qb_data())
    #         data.append(qb_data)
    #     return data
    '''<- 18.03'''
    ''' ****************************************************************** '''
    ''' ******* extracting rubik's portions ******* '''
    
    def layers(self, ax):
        """Cut rubik in layers of given axis ax and return them as an array of arrays"""
        return list(map(lambda x: np.squeeze(x), np.split(self.rubik, np.arange(1, self.shape[ax]),axis=ax)))


    def edge(self, l1, l2):
        '''Return qbs common to given layers (qbs on the edge of layers)'''
        layer1 = l1.flatten()
        layer2 = l2.flatten()
        border = []
        for i in layer1:
            for j in layer2:
                #if for some reason qb return anything customized, it won't work
                if (i==j):
                    border.append(i)
        return border


    def get_face(self, l, *coord):
        if len(l.shape)>1:
            return np.array(list(map(lambda x: x.get_face(*coord), l.flatten()))).reshape(l.shape)
        else:
            return list(map(lambda x: x.get_face(*coord), l))
        
    ''' ****************************************************************** '''
    ''' *** converting numbers, for example, into string representation *** '''
    ''' *** i should handle them somewhere outside this class *** '''

    def interpret_rubik_layer(self, interpreter, l, *coord):
        '''Return a part of the qb array and represent it using a given dictionary'''
        return np.array(list(map(lambda x: x.interpret_qb(interpreter, *coord), l.flatten()))).reshape(l.shape)


    def print_faces_interpret(self, interpreter):
        for ax in range(self.num_axis):
            rubik_layers = self.layers(ax)
            for side in self.sides:
                layer = rubik_layers[side]
                print(ax, side)
                print(self.interpret_rubik_layer(interpreter, layer, ax, side))

    ''' ****************************************************************** '''
    ''' ******* changing positions of the qbs in rubik ******* '''

    def rotate(self, ax, l, direction):
        '''
        Rotate a layer l around an axis ax in a given direction. As  a positive 
        direction (=1) is considered a counterclockwise rotation.
        '''
        def check_right_hand_rule(rot_axis):
            '''
            To ensure a rotation in the right direction, this method calculates 
            a cross product of the remaining unit vectors, witch are in a plane 
            of rotation.
            '''
            unit_vectors = [[1,0,0], [0,1,0], [0,0,1]]
            unit_vectors = np.delete(unit_vectors, rot_axis, axis=0)
            return np.cross(unit_vectors[0],unit_vectors[1])[rot_axis]
        

        layers = self.layers(ax)
        
        # Note that mapping through qb instances changes the originals in the self.rubik.
        list(map(lambda qb: qb.flip(ax,direction), layers[l].flatten()))
        
        #Calculate accual direction od rotation. true_dir isn't passed to small 
        #cubes, because the same correction is made in qb's method.
        dir_correct = check_right_hand_rule(ax)
        true_dir = direction * dir_correct
        layers[l] = np.rot90(layers[l], k=true_dir)
        self.rubik = np.stack(layers, axis=ax)
        self.rubik_val_update()
        
        
    # @functools.lru_cache()
    # def rot(self, *data):
    #     self.rotate(*data)
    #     val = self.calc_rubik_value()
    #     return val
        

    def flip(self, ax, direction):
        '''
        Rotation of all layers of the axis ax in the same direction
        '''
        for l in range(self.shape[ax]):
            self.rotate(ax, l, direction)
        
     
    def rand_rotate(self):
        rand_ax = random.randint(0, len(self.shape)-1)
        rand_la = random.randint(0, self.shape[rand_ax]-1)
        rand_dir = random.randint(0, 1)*2 - 1
        self.rotate(rand_ax, rand_la, rand_dir)
        
        return (rand_ax, rand_la, rand_dir)
        # val, std = self.calc_rubik_value()
        # return (val, std)
     
    def mix(self, chaos, deviation):
        val, std = self.calc_rubik_value()
        i=0
        while not ((val > chaos) and (std < deviation)):
            i+=1
            if i > 100:
                break;
            
            # val, std = self.rand_rot()
            self.rand_rotate()
            val, std = self.calc_rubik_value()
            
    def mix_n(self, n):
        for i in range(n):
            val, std = self.rand_rotate()
            # print(val, std)
            

    ''' ****************************************************************** '''
    ''' ******* determining the degree of solution of rubik's cube ******* '''

    def calc_rubik_value(self):
        
        def entropy(face_counter):
            '''
            A measure of disorder, calculated using the equation:
            S = - sum(p(x)*log_10(p(x)))
            
            Entropy is normalized to the range (0,1), where:
              1 - maximum disorder
              0 - no disorder (i.e. all input values are the same)       
            '''

            choices = self.num_axis * self.num_sides
            uniform_prob = 1/choices
            # Note: S = -sum(p(x)*log_10(p(x))) = -p(x)*log_10(p(x))*choices = -log_10(p(x))
            max_entropy = -1 * np.log10(uniform_prob)
            
            count_sum = sum(face_counter.values())
            face_info = face_counter.most_common()
            count_prob = list(map(lambda x: x[1]/count_sum, face_info))
            entropy_list = list(map(lambda x: x*np.log10(x), count_prob))
            entropy = -1 * sum(entropy_list)
            norm_entropy = entropy/max_entropy
            return norm_entropy
        
        def face_color_value():
            '''
            A naive calculation of a Rubik's cube. Calculate the degree of 
            disorder of the values of each face independently, without checking 
            the centres of the faces, neighbouring qb or adjacent layers.
            Return list of normalised values of cube faces.
            '''
            face_val = []
            for ax in range(self.num_axis):
                rubik_layers = self.layers(ax)
                for side in self.sides:
                    layer = rubik_layers[side]
                    face = self.get_face(layer, ax, side).flatten()

                    count = Counter(face)
                    f_entropy = entropy(count)
                    face_val.append(f_entropy)
            return face_val

        def face_middle_value():
            '''
            Calculate the value of the rubik's cube in respect to the layers qb
            and based on the number (color) in the centre of the face.  
            Determine the value of each layer and add them up to get the 
            value of the whole cube. Works only for rubik with an odd number 
            of layers. 
            
            '''
            value_dict = {
                0: -1,      # no match
                1: 1,       # correct value on adjasent layer
                2: 2,       # correct value on examined layer
                3: 'error'  # it wolud mean a qb with 2 faces with tje same value
                }
            
            
            rubik_val = np.zeros_like(self.rubik)
            for ax in range(self.num_axis):
                rubik_layers = self.layers(ax)
                rubik_val_layers = list(map(lambda x: np.squeeze(x), np.split(rubik_val, np.arange(1, rubik_val.shape[ax]),axis=ax)))
                for side in self.sides:
                    layer = rubik_layers[side]
                    val_layer = rubik_val_layers[side]
                    face = self.get_face(layer, ax, side)
                    # print(ax, side)
                    # print(face)
                    middle = face[int(face.shape[0]/2), int(face.shape[1]/2)]
                    
                    face_val = np.zeros_like(face)
                    #print(face_val)
                    
                    for a in range(self.num_axis):
                        for s in self.sides:
                            if not ax == a:
                                coord = [s, slice(None)]

                                edge = layer[tuple(coord)]
                                adj_val = self.get_face(edge, a, s)
                                
                                if (self.no_val in adj_val):
                                    coord.reverse()
                                    edge = layer[tuple(coord)]
                                    adj_val = self.get_face(edge, a, s)
                                    
                                layer_val = self.get_face(edge, ax, side)
                                
                                # print(layer_val)
                                # print(adj_val)
                                
                                #create lists of booleans
                                layer_check = layer_val == middle
                                adjasent_check = adj_val == middle
                                bit_values = np.column_stack((layer_check, adjasent_check))
                                #create bitarry and convert on fly to int
                                flags = list(map(lambda x: ba2int(bitarray(list(x))), bit_values))
                                values = list(map(lambda x: value_dict[x], flags))
                                
                                '''
                                #create lists of booleans and convert to int
                                layer_check = layer_val == middle
                                layer_check = list(map(int, layer_check))
                                adjasent_check = adj_val == middle
                                adjasent_check = list(map(int, adjasent_check))
                                
                                bit_values = np.column_stack((adjasent_check, layer_check))
                                flags = list(map(lambda x: np.packbits(x, bitorder='little').item(), bit_values))
                                values = list(map(lambda x: value_dict[x], flags))
                                '''
                                
                                # print("----------")
                                # print(face_val)
                                fv = np.sum((face_val[tuple(coord)], values), axis=0)
                                face_val[tuple(coord)] = fv
                                # print(face_val)
                                # print("(#######################################)")
                    
                    val_layer = val_layer + face_val
                    # print()
                    rubik_val_layers[side] = val_layer
                rubik_val = np.stack(rubik_val_layers, axis = ax)
                # print(rubik_val)
                # print("--------------")
                

            return rubik_val

        fcv = face_color_value()
        
        how_solved = (np.average(fcv), np.std(fcv))
        rubik_val = face_middle_value()
        
        # print(rubik_val)
        
        return (how_solved, rubik_val)
    
    
    def rubik_val_update(self):
        self.how_solved, self.rubik_val = self.calc_rubik_value()
    
    
    ''' ****************************************************************** '''
    ''' ****************************************************************** '''
   
            
if __name__ == '__main__':
    colors = {
        0: "Black",     # HIDDEN
        1: "Green",     # RIGHT
        2: "Blue",      # LEFT
        3: "Red",       # FRONT
        4: "Orange",    # BACK
        5: "Yellow",    # DOWN
        6: "White",     # UP
    }
    r = Rubik()

    # r.mix(0.8, 0.05)
    r.rotate(1, 0, 1)
    print(np.sum(r.rubik_val))
    #r.calc_rubik_value()
    #print(r.get_rubik())
    '''
    print(r.rotate(0,0,-1))
    print(r.rotate(1,0,1))
    print(r.rotate(0,1,-1))
    print(r.rotate(2,0,1))
    print(r.rotate(0,0,1))
    '''

