ez_trans
========

fast easy files transfer, by python[v3.3.2].

suitable for build or millions of trivial files sync e.g. 

speed up a lot comparing to direct robocopy/xcopy in slow network connection environment. 
In our practice it takes ~30 mintues for 2GB (tens of thousands files) using ez_trans vs.
 6-7 hours via robocopy (multi-threaded), from site A to site B.
 
SiteA --- (~200KB/s) --> Site B

<b>Usages:</b>

 1. config inside python file, refer to test.py as a sample
 
 2. config via ini file, refer to test_ini.py as a sample
 
<b>The simple concept behind:</b>

 utilize a machine on Site A as mediator which has excellent network connection with storage server in the same site, 
 
 detect and compress the build/folder into volumes, and then upload to a FTP server on site B in concurrent way.
 
<b>Requirement:</b>

 1. 7-zip command line utility accessible in command line
 2. Machine M on site A as mediator, where the script will run on
 3. FTP server on site B
 
<b>Configuration:</b>
 a. python way:

    from ez_trans  import monitor, config, logger
  
    log = logger.SimpleLogger()
    log.log("hello, welcome to ethan's easy file transfer.\n")
    
    cfg = config.config()

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

b. ini way:

refer to monitor_cfg.ini

test_ini.py looks like this:

    from ez_trans import monitor, config, logger

    print ("hello welcome to ethan's easy file transfer.\n")
    ini = 'monitor_cfg.ini'
    print ("using ini file %s to config.\n"%ini)

    cfg = config.config()
    cfg.load(ini)

    mont = monitor.monitor(cfg)
    mont.start()
