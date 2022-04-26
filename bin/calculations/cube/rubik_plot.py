import numpy as np
import matplotlib.pyplot as plt


class RubikHistory():
    def __init__(self, rubik):
        
        self.num_axis = rubik.num_axis
        self.num_faces = rubik.num_sides
        self.num_faces = self.num_axis * self.num_sides
        ''' Calculated in rubik '''
        #fit value of qbs
        self.qb_val = []
        #entropy calculation. Tuple of a value and a standard deviation
        self.entropy_val = []        
        
        ''' Calculated in this module '''
        #sum of qb values of the rubik faces
        self.faces_val = []
        #sum of values of every qb
        self.rubik_val = []

        
    def add_data(self, *d):
        qbs, entropy = d
        self.qb_val.append(qbs)
        self.entropy_val.append(entropy)
        
        
    def calc_val(self, d):
        qbs = d
        for ax in range(self.num_axis):
            layers = list(map(lambda x: np.squeeze(x), np.split(val, np.arange(1, shape[ax]),axis=ax)))
            faces.append(np.sum(layers[0]))
            faces.append(np.sum(layers[-1]))

    
    def plot(self):
        fig, ax = plt.subplots(2,1)
        for i in range(self.faces_num):
            ax.plot(self.data)

        plt.show()
        