import numpy as np

class Calculator:
    def __init__(self, network):
        self._network = network

    # step 3: find index j
    def compute_closest_representative(self):
        for i, representative in enumerate(self._network.representatives):

            # compute euclidean distance for every representative
            representative.distance = np.linalg.norm(np.asarray(self._network.inputs) - np.asarray(representative.weight))

            if i == 0:
                min_dist_value = representative.distance
                min_dist_index = 0
            elif representative.distance < min_dist_value:
                min_dist_index = i

        self._network.closest_representative = self._network.representatives[min_dist_index]

    # step 4: update wj
    def compute_new_weight(self):
        if self._network.input_data_class == self._network.closest_representative.data_class:
            # wjnew = wjold + alpha(x - wjold)
            self._network.closest_representative.weight = np.add(self._network.closest_representative.weight, np.multiply(self._network.alpha, (np.subtract(self._network.inputs, self._network.closest_representative.weight)))).tolist()
        else:
            # wjnew = wjold - alpha(x - wjold)
            self._network.closest_representative.weight = np.subtract(self._network.closest_representative.weight, np.multiply(self._network.alpha, (np.subtract(self._network.inputs, self._network.closest_representative.weight)))).tolist()

