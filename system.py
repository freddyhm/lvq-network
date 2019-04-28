from network import Network
from calculator import Calculator
from utility import Utility
from logger import Logger
import random

class System:
    def __init__(self):
        self._utility = None
        self._network = None
        self._calculator = None
        self._logger = None
        self._performance_rate = ""
        self._data = None
        self._data_learning = None
        self._data_vc = None
        self._data_gen = None
        self._data_test = None
        self._data_size = 0
        self._success_count = 0
        self._data_processed_count = 0

    def build(self):
        self.load_helpers()
        self._network = Network()

        # step 0: initialize alpha
        self._network.alpha = 0.01 if self._config["alpha"][0] == "decrement" else self._config["alpha"][0]

        self._logger = Logger(self._network, self._config["saved_network_path"][0])
        self._calculator = Calculator(self._network)

        # make sure our random numbers stay the same
        random.seed(1)

    def load_helpers(self):
        self._utility = Utility("config.txt")
        self._config = self._utility.load_config()


    def load_data(self, data_type, mode):

        if data_type == None:
            if mode == "learn":
                data_path = "training_data_path"
            elif mode == "vc":
                data_path = "vc_data_path"
            elif mode == "generalization":
                data_path = "gen_data_path"

            data_type = self._utility.load_data(self._config[data_path][0], mode)

        return data_type

    # major steps for algorithm
    def run(self, mode):

        # load data depending on mode/step
        if mode == "learn":
            self._data_learning = self.load_data(self._data_learning, mode)
            self._data = self._data_learning
            self._data_size = 1340
            # Step 0: initiliaze representatives and weights
            self.set_representatives()
        elif mode == "vc":
            self._data_vc = self.load_data(self._data_vc, mode)
            self._data = self._data_vc
            self._data_size = 120
        elif mode == "generalization":
            self._data_gen = self.load_data(self._data_gen, mode)
            self._data = self._data_gen
            self._data_size = 780

        epoch = self._config["epoch"][0] if mode == "learn" else 1

        k = 0

        # Step 1 & 6: continue to steps 2 - 6 unless stop criteria has been reached
        if mode == "learn" and self._config["alpha"][0] == "decrement":
            # reduce alpha after each epoch
            while self._network.alpha > 0.001:
                self.run_epoch(mode)
                print(self._logger.log_performance(mode, str(k + 1), self._success_count, self._data_processed_count,
                                                   self._performance_rate))
                k += 1
        else:
            while k < epoch:
                self.run_epoch(mode)
                print(self._logger.log_performance(mode, str(k + 1), self._success_count, self._data_processed_count,
                                                  self._performance_rate))
                k += 1
                
        print("Sauvegarde des donnees utilisee...")
        self._logger.log_learning_db(self._config["saved_learning_db_path"][0], self._data)
            
            
    def run_epoch(self, mode):
    
        # reset so we get a new performance rate for every epoch
        self._success_count = 0
        self._data_processed_count = 0
        self._performance_rate = ""

        i = 0

        # Step 2: iterate through each input in data file
        while i < self._data_size:
            print("Iteration:" + str(i))
            self.run_iteration(mode)
            i += 1

        if mode == "learn":
            self._network.alpha = self._network.alpha / self._config["alpha_divider"][0]

    def run_iteration(self, mode):
        # set a random input for our network
        self.set_io()
    
        # Step 3: find representative closest to input
        self._calculator.compute_closest_representative()
    
        # Step 4: update weight
        if mode == "learn":
            self._calculator.compute_new_weight()
    
        self.check_prediction()

        # keep count of performance
        self._data_processed_count += 1
        self._performance_rate = self._utility.get_performance_rate(self._success_count,
                                                              self._data_processed_count)
        print(str(self._performance_rate))

    def set_representatives(self):
        # initialize weights with either cmean method or random representative method
        rep_data = self._utility.get_representatives(self._data)
        self._network.build_representatives(rep_data)

    def set_io(self):
        rand_data_class = random.choice(list(self._data))
        self._network.inputs = random.choice(self._data[rand_data_class]["input"])
        self._network.input_data_class = rand_data_class

    def check_prediction(self):
        # keep track of our successes so we can return a performance rate
        if self._network.input_data_class == self._network.closest_representative.data_class:
            self._success_count += 1

    def save(self):
        self._logger.log_network(self._network)

    def save_performance(self):
        self._logger.write_performance()

    # used to print performance in main
    @property
    def performance_rate(self):
        return self._performance_rate