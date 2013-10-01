'''
Created on Mar 6, 2013

@author: ethan liu
'''

from ez_trans  import monitor, config, logger

def exec():   
    log = logger.SimpleLogger()
    log.log("hello, welcome to ethan's easy file transfer.\n")
    
    cfg = config.config({})

    cfg.key = "test"
    cfg.base_dir='p:/builds'
    cfg.pattern='11.??.0.0'
    cfg.time_out = 30*60

    trans_item = config.config.trans_item()
    trans_item.relative_path = 'DVD'
    trans_item.zip_name = 'DVD.7z'
    trans_item.volume_size = '18m'
    cfg.trans_items.append(trans_item)

    target = config.config.ftp_target()
    target.server = '127.0.0.1'
    target.user='qtp'
    target.password='qtpdev'
    target.relative_path = 'builds/'
    
    cfg.trans_target = target

    cfg.working_folder = 'c:/test_ez_trans'

    mont = monitor.monitor(cfg)
    mont.start()

if __name__ == '__main__':
    exec()

