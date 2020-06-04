import os
import numpy as np
import pickle
import math
from utils import utils


class LogSimilarityCalculator:

    def __init__(self, block_to_split=10, min_log_number_in_block=1, folder=""):
        self.block_to_split = block_to_split
        self.min_log_number_in_block = min_log_number_in_block
        self.folder = folder
        self.weights = None
        self.softmax_weights = None
        if folder.strip() != "":
            self.load_model(folder)

    def load_model(self, folder):
        self.folder = folder
        if not os.path.exists(os.path.join(folder, "weights.pickle")):
            return
        with open(os.path.join(folder, "weights.pickle"), "rb") as f:
            self.block_to_split, self.min_log_number_in_block, self.weights, self.softmax_weights =\
                pickle.load(f)
        if not os.path.exists(os.path.join(folder, "config.pickle")):
            return
        try:
            with open(os.path.join(folder, "config.pickle"), "wb") as f:
                self.config = pickle.load(f)
        except: # noqa
            pass

    def add_config_info(self, config):
        self.config = config

    def save_model(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)
        if self.weights is not None:
            with open(os.path.join(folder, "weights.pickle"), "wb") as f:
                pickle.dump([self.block_to_split, self.min_log_number_in_block,
                             self.weights, self.softmax_weights], f)
            try:
                if self.config:
                    with open(os.path.join(folder, "config.pickle"), "wb") as f:
                        pickle.dump(self.config, f)
            except: # noqa
                pass

    def message_to_array(self, detected_message_res, stacktrace_res):
        all_lines = [" ".join(utils.split_words(detected_message_res))]
        split_log_lines = utils.filter_empty_lines(
            [" ".join(utils.split_words(line)) for line in stacktrace_res.split("\n")])
        split_log_lines_num = len(split_log_lines)
        data_in_block = max(self.min_log_number_in_block,
                            math.ceil(split_log_lines_num / self.block_to_split))
        blocks_num = math.ceil(split_log_lines_num / data_in_block)

        for block in range(blocks_num):
            all_lines.append("\n".join(
                split_log_lines[block * data_in_block: (block + 1) * data_in_block]))
        if len([line for line in all_lines if line.strip() != ""]) == 0:
            return []
        return all_lines

    def weigh_data_rows(self, data_rows, use_softmax=False):
        padded_data_rows = np.concatenate([data_rows,
                                           np.zeros((max(0, self.block_to_split + 1 - len(data_rows)),
                                                    data_rows.shape[1]))], axis=0)
        result = None
        if use_softmax:
            result = np.dot(np.reshape(self.softmax_weights, [-1]), padded_data_rows)
        else:
            result = np.dot(np.reshape(self.weights, [-1]), padded_data_rows)
        return np.clip(result, a_min=0, a_max=1)
