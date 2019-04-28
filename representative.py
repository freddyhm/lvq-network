class Representative:
    def __init__(self, representative_id, data_class, distance=0, weight=[]):
        self._representative_id = representative_id
        self._data_class = data_class
        self._weight = weight
        self._distance = distance

    @property
    def data_class(self):
        return self._data_class

    @property
    def representative_id(self):
        return self._representative_id

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, distance):
        self._distance = distance
