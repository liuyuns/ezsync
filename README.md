ez_trans
========

easy fast files transfer, by python, suitable for build or millions of trivial files sync e.g. 
speed up a lot comparing to direct robocopy/xcopy in slow network connection environment. 
In our practice it takes ~30 mintues for 2GB (tens of thousands files) using ez_trans vs.
 6-7 hours via robocopy (multi-threaded), from site A to site B.
SiteA --- (~200KB/s) --> Site B

Usages:
 config inside python file, refer to test.py as a sample
 config via ini file, refer to test_ini.py as a sample
 
The concept is simple:
 utilize a machine on Site A as mediator which has excellent speed connect to storage server in the same site, 
 detect and compress the build/folder into volumes, and then upload to a FTP server on site B in concurrent way.
 
Requirement:
 1. 7-zip command line utility
 2. Machine M on site A as mediator
 3. FTP server on site B
 
Configuration:
 a. python way:
======>
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
<=====

b. ini way:

monitor_cfg.ini

===>
[basic]
key = build
base_dir = p:\builds
pattern = 11.??.0.0
; a file or folder indicates that we can start transfer
; e.g. after detect folder p:\builds\11.18.0.0,
; it will continue to wait and then transfer till p:\builds\11.18.0.0\log\pass.ini presents
ready_indicator = build\log\pass.ini
; time out if ready indicator not presents till the pre-defined seconds pass
; 0 - no time out
time_out = 1800
; seconds delay before really launch transfer since ready indicator detected
delay_before_trans = 10
; local working folder on the machine that running the script
working_folder = g:\ez_trans\working
start_hour = 0
end_hour = 24

[trans]
;the path to compress and then transfer
relative_path = DVD
zip_name = DVD.7z
; set volume size to 0 to suppress the creation of volumes. acceptable formats: {size}[b|k|m|g]
volume_size = 18m

; defines the FTP server and location to store compressed file
[target]
server = 127.0.0.1
user = test
password =  
relative_path = /builds/

<====

test_ini.py
====>
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
<====
