import os, glob, time
from ez_trans import monitor, config, logger


def exec():

    print ("hello welcome to ethan's easy file transfer.\n")
    ini = 'monitor_cfg.ini'
    print ("using ini file %s to config.\n"%ini)

    cfg = config.config()
    cfg.load(ini)

    mont = monitor.monitor(cfg)
    mont.start()

if __name__ == "__main__":
    exec()


