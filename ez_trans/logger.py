import threading

class logger(object):
    """description of class"""
    def log(self, message, level='debug'):
        pass

    def error(self, message):
        pass
    def warn(self, message):
        pass   
    def message(self, message):
        self.log(message)
        pass

class log_prxoy(object):
    loggers = []
    def __init__(self, logger = None):
        if logger:
            loggers.append(logger)
    def attachlistener(self, logger):
        if logger:
           loggers.append(logger)
        pass

    def message(self, message):
        pass
    def warn(self, message):
        pass
    def error(self, message):
        pass

class SimpleLogger(logger):
    def log(self, message, level='debug'):
        level_indicator = '' if level == 'debug' or level == None else '#%s# '%level
        print ("[tid:%d] - %s%s"%(threading.current_thread().ident, level_indicator, message))

    def error(self, message):
        self.log (message, level="error")
        pass
    def warn(self, message):
        self.log (message, level="warn")


