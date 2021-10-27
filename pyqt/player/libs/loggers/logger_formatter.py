
import inspect
import os


class LoggerFormatter:

    def __init__(self, json_logger, std_logger):
        self.std_logger = std_logger
         # self.json_logger = json_logger
        self.dut_info = {}
        self.log_dict = {}
        self._formatted_log = {}

    def _get_formatted_log(self, msg):
        frame = inspect.stack()[2]
        module = inspect.getmodule(frame[0])
        info = inspect.getframeinfo(frame[0])

        self.log_dict["line"] = info.lineno
        self.log_dict["module"] = os.path.basename(module.__file__)
        self.log_dict["msg"] = msg

        self._formatted_log = {"dutInfo": self.dut_info, "log": self.log_dict}

    def debug(self, msg):
        self._get_formatted_log(msg)
        self.std_logger.debug(self._formatted_log)
         # self.json_logger.debug(self._formatted_log)

    def info(self, msg, resp_log=None):
        self._get_formatted_log(msg)

        formatted_info_log = {"dutInfo": self.dut_info, "log": self.log_dict, "respLog": resp_log}
        self.std_logger.info(formatted_info_log)
         # self.json_logger.info(formatted_info_log)

    def warning(self, msg):
        self._get_formatted_log(msg)
        self.std_logger.warning(self._formatted_log)
         # self.json_logger.warning(self._formatted_log)

    def warn(self, msg):
        self._get_formatted_log(msg)
        self.std_logger.warn(self._formatted_log)
         # self.json_logger.warn(self._formatted_log)

    def error(self, msg):
        self._get_formatted_log(msg)
        self.std_logger.error(self._formatted_log)
         # self.json_logger.error(self._formatted_log)

    def critical(self, msg):
        self._get_formatted_log(msg)
        self.std_logger.critical(self._formatted_log)
         # self.json_logger.critical(self._formatted_log)

    def log(self, msg):
        self._get_formatted_log(msg)
        self.std_logger.log(self._formatted_log)
         # self.json_logger.log(self._formatted_log)
