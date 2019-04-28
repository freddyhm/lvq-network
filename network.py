
from representative import Representative

class Network:
    def __init__(self):
        self._representatives = []
        self._alpha = 0
        self._input_data_class = 0
        self._inputs = []
        self._closest_representative = None
        
    @property
    def closest_representative(self):
        return self._closest_representative

    @closest_representative.setter
    def closest_representative(self, closest_representative):
        self._closest_representative = closest_representative

    @property
    def input_data_class(self):
        return self._input_data_class

    @property
    def representatives(self):
        return self._representatives

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    def rep_data(self):
        return self._rep_data

    @rep_data.setter
    def rep_data(self, rep_data):
        self._rep_data = rep_data

    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha

    @property
    def input_data_class(self):
        return self._input_data_class

    @input_data_class.setter
    def input_data_class(self, input_data_class):
        self._input_data_class = input_data_class

    def build_representatives(self, rep_data):
        for data_class, inputs in rep_data.items():
            for i, rep in enumerate(inputs["reps"]):
                id = data_class + "-" + str(i + 1)
                representative = Representative(id, data_class, 0, rep)
                self._representatives.append(representative)





