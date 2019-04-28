import re
from cmean import CMean
from tqdm import tqdm
import time
import random

class Utility:
    def __init__(self, path):
        self._config = {}
        self._data = {}
        self._path = path
        self._timers = {}

    def load_data(self, data_path, mode):
        self._data = {}
        
        # must tell progress bar how many lines to load
        print("Chargement des donees")
        file_size = 0
        if mode == "learn":
            file_size = 1340
        elif mode == "vc":
            file_size = 120
        elif mode == "generalization":
            file_size = 780

        with open(data_path) as filestream:
            for line in tqdm(filestream, total=file_size, unit="data"):
                line_data = line.split(": ")        
                line_element_data = line_data[1].split(" ")
                # keep static params in new list
                line_extracted_data = [] 
                start = 0
                end = 26 if self._config["param_type"][0] == "all" else 12 
                frame_size = 26
                num_of_frames = self._config["frames"][0]
                frame_total = frame_size * num_of_frames
                # extract params for every frame
                for idx in range(0, frame_total, frame_size):
                    line_extracted_data += line_element_data[start:end]
                    start += frame_size
                    end += frame_size

                # format data to be a data structure of all inputs categorized by what they represent
                # ex: "1" => "inputs:" [[3,-4,-10], [6,9,-0.3], ...]
                key_name = line_data[0]
                self.format_data(line_extracted_data)
                self._data.setdefault(key_name, {"input": []})["input"].append(line_extracted_data)

        return self._data
        
    def load_config(self):
        # read file and extract data
        with open(self._path) as filestream:
            for line in filestream:
                key_name = ""
                line_data = line.split(": ")
                line_element_data = line_data[1].split(" ")
                key_name = self.get_key_name(line_data[0])

                # add selected properties to our config structure 
                if key_name != "undefined":
                    self.format_data(line_element_data)
                    self._config[key_name] = line_element_data

        return self._config

    def format_data(self, line_element_data):
        for idx, element in enumerate(line_element_data) :
            if element != "" and element != " " and element != "\n":
                # remove all non-digits, non-alpha characters
                element = element.rstrip()
                element = element.strip()

                # convert strings into float and int when necessary
                if re.search("\d+\.\d+", element): 
                    element = float(line_element_data[idx])
                elif re.search("\d", element):
                    element = int(line_element_data[idx])    
                 
                line_element_data[idx] = element
            else:
                del line_element_data[idx]
    
    # map parameter names in config file to keys we can use
    def get_key_name(self, line_param_name):
        if line_param_name == "Dimension of input [frames x static/all]":
            key_name = "dim_input"
        elif line_param_name == "alpha [0.01][0.1][...][decrement = 0.01 to 0.001]":
            key_name = "alpha"
        elif line_param_name == "Epoch":
            key_name = "epoch"
        elif line_param_name == "Number of frames to extract":
            key_name = "frames"
        elif line_param_name == "Load static parameters or all parameters [static = 12][all = 26]":
            key_name = "param_type"
        elif line_param_name == "Training data path":
            key_name = "training_data_path"
        elif line_param_name == "Initial weight interval":
            key_name = "init_weight_interval"
        elif line_param_name == "VC data path":
            key_name = "vc_data_path"
        elif line_param_name == "Generalization data path":
            key_name = "gen_data_path"
        elif line_param_name == "Number of classes":
            key_name = "num_classes"
        elif line_param_name == "Number of representatives per class":
            key_name = "num_representatives"
        elif line_param_name == "Saved network snapshot file":
            key_name = "saved_network_path"
        elif line_param_name == "Saved database used for learning":
            key_name = "saved_learning_db_path"
        elif line_param_name == "Initialize weight method [cmean][random]":
            key_name = "weight_method"
        elif line_param_name == "Alpha divider for each epoch (only with decrement option)":
            key_name = "alpha_divider"
        else:
            key_name = "undefined"
        return key_name

    def get_performance_rate(self, success_num, total_data):
        return (success_num / total_data) * 100


    def get_representatives(self, data):

        rep_data = {}

        num_reps = self._config["num_representatives"][0]

        print("\nCreation des representants")

        # format data to be a data structure of all inputs categorized by what they represent
        # ex: "1" => "inputs:" [[3,-4,-10], [6,9,-0.3], ...]

        # cmean implementation
        if self._config["weight_method"][0] == "cmean":
            num_dimensions = self._config["dim_input"][0]
            diff_max = 100
            threshold = .000001

            for key, value in tqdm(data.items()):
                reps = CMean(value["input"], num_dimensions, num_reps, diff_max, threshold)
                rep_data.setdefault(key, {"reps": None})["reps"] = reps
        elif self._config["weight_method"][0] == "random":

            #
            random.seed(1)
            for key, value in tqdm(data.items()):
                reps = []
                for representative in range(num_reps):
                    reps.append(random.choice(value["input"]))

                rep_data.setdefault(key, {"reps": None})["reps"] = reps

        return rep_data

    def start_timer(self, timer_name):
        self._timers[timer_name] = time.time()

    def end_timer(self, timer_name):
        self._timers[timer_name] = time.time() - self._timers[timer_name]


    @property
    def timers(self):
        return self._timers

