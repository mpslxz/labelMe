import os
import glob
import json
import time


class LogFactory(object):

    def __init__(self, file_root):
        """Keeps track of the labelled files and labeling sessions.
        The log file is a CSV that indicates the file path and labelling dates.

        :param log_path: Path to the log file
        :param file_paths: File paths
        :returns: LogFactory object
        :rtype: LogFactory

        """
        self.file_root = file_root
        self.log_name = 'activity_log.json'

        if not os.path.exists(self.log_name):
            self._initialize_log_file()
        else:
            with open(self.log_name, 'r') as f:
                self.log = json.load(f)

    def _initialize_log_file(self):
        file_path = glob.glob(self.file_root + "/**/*.b8")
        init_dates = ['null' for i in range(len(file_path))]
        data = file_path
        self.log = {k: v for k, v in zip(data, init_dates)}
        self.log['root'] = self.file_root
        self.write_log()

    def get_pending_files_list(self):
        return [k for k in self.log if self.log[k] == 'null']

    def write_log(self):
        with open(self.log_name, 'w') as f:
            json.dump(self.log, f)

    def stamp(self, path):
        self.log[path] = time.asctime(time.localtime(time.time()))
