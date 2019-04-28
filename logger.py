import json
from tqdm import tqdm 
class Logger:

    def __init__(self, network, path):
        self._path = path
        self._network = network
        self._log_output = ""
        self._performance_output = ""

    def reset(self):
        self._log_output = ""


    def log_network(self, network): 
        self._log_output += self._performance_output
        for representative in tqdm(network.representatives):
            self.log_representative(representative)
            
        self.write()

    def log_representative(self, representative):
        self._log_output +="----------------------------------\n"
        self._log_output += "Representative id: " + representative.representative_id + "\n"
        self._log_output +="----------------------------------\n"
        self._log_output += "Class: " + str(representative.data_class) + "\n"
        self._log_output += "Weight: " + json.dumps(representative.weight) + "\n"
        self._log_output += "Distance: " + str(representative.distance) + "\n"
        self._log_output +="----------------------------------\n"

    def log_performance(self, mode, num_epoch, success, num_learning_data, learning_rate):

        self._performance_output +="---------------------------------------------------\n"
        self._performance_output +="Mode: " + mode + "\n"
        self._performance_output +="---------------------------------------------------\n"
        self._performance_output +="Taux de succes: (nb de succes / nb de donnee) * 100\n"
        self._performance_output +="---------------------------------------------------\n"
        self._performance_output +="Epoque: " + str(num_epoch) + "\n"
        self._performance_output +="Nb de succes: " + str(success) + "\n" 
        self._performance_output +="Nb de donnee: " + str(num_learning_data) + "\n"
        self._performance_output +="Taux: " + str(learning_rate) + "%\n"
        self._performance_output +="---------------------------------------------------\n"
        
        return self._performance_output


    def log_learning_db(self, learning_db_path, data):
        
        log_data_output = ""
        with open(learning_db_path, "w") as out:

            log_data_output +="----------------------------------\n"
            log_data_output += "Base de donnee d'apprentissage\n"
            log_data_output +="----------------------------------\n"

            for data_class, inputs in tqdm(data.items()):
                log_data_output += json.dumps(data_class) + "\n"
                for data in inputs["input"]:
                    log_data_output += json.dumps(data) + "\n"

            out.write(log_data_output)

    def write(self):
        with open(self._path, "w") as out:
            out.write(self._log_output)

    def write_performance(self):
        with open("performance-output.txt", "w") as out:
            out.write(self._performance_output)