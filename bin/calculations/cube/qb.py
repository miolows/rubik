import numpy as np

class Qb():
    def __init__(self, pos, shape=(3,2)):
        self._shape = shape
        self._qb = np.zeros(self._shape)
        '''18.03 ->'''
        self.position = pos  #needed in visualisation
        '''<- 18.03'''
    
    ''' *** setter and getters *** '''
    
    def set_qb(self, c, *coord):
        self._qb[coord] = c
        return self._qb[coord]
    
    def get_qb(self):
        return self._qb
    
    def get_qb_data(self):
        data = []
        for q in self._qb:
            data.append(q)
        return data
    
    def get_face(self, *coord):
        return self._qb[coord]
    
    '''18.03 ->'''
    def get_position(self):
     return self.position #needed in visualisation
    '''<- 18.03'''
    
    def interpret_qb(self, interpreter, *coord):
        '''Return a part of the qb array and represent it using the dictionary'''
        s_qb = np.array(list(map(lambda x: interpreter[x], self._qb[coord].flatten())))
        return s_qb
    
    ''' ****** '''

    def flip(self, xyz, direction):
        '''
        Rotate faces in the plane perpendicular to axis of 
        rotation.
        Note: this algorithm does not calculate rotation in the 
         
        Parameters
        ----------
        xyz : int
             axis of rotation
        direction : 0, 1 or -1
            0 - pass
            1 - counterclockwise flip
           -1 - clockwise flip
        '''
        
        def check_right_hand_rule (ax):
            '''
            To ensure rotation in the right direction, this method calculates the 
            cross product of the remaining unit vectors, witch are in plane of rotation
            '''
            unit_vectors = [[1,0,0], [0,1,0], [0,0,1]]
            unit_vectors = np.delete(unit_vectors, ax, axis=0)
            return np.cross(unit_vectors[0],unit_vectors[1])[ax]

        if not direction:
            pass
        else:
            if (direction ** 2 - 1):
                raise Exception("wrong value of direction. Must be 1 or -1")
            
            # If someone wonders what is going on, I can tell that it just 
            # works (at least for cube). And it is sexy-short code, quite 
            # effitient (putting aside this cross product calculations)
            d = direction * check_right_hand_rule(xyz)
            const_f = self._qb[xyz]
            changed_f = np.delete(self._qb, xyz, axis=0)
            changed_f = np.roll(changed_f.T,d).T
            new_qb = np.insert(changed_f, xyz, const_f, axis=0)
            
            self._qb = new_qb
            

    


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
    q = Qb(0)
    print(q)
    print(q.get_qb_data())