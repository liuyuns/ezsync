import os, time, datetime, glob, threading
from ez_trans import logger

def sort_by_time(paths):
    """
    sort passed-in path array according the last modified time
    """
    mtime = lambda path: os.path.getmtime(path)
    return list(sorted(paths, key=mtime))

class monitor(object):
    """
    A monitor class.
    """
    monitoring = True
    last_trans_folder = None
    thread = None
    logger = logger.SimpleLogger()

    from ez_trans.config import config
    def __init__(self, config, logger = None):  
        if logger:
            self.logger = logger      
        self.config = config
        self.pattern = os.path.join(self.config.base_dir, self.config.pattern)
        self.logger.message("monitor folder pattern:%s"%self.pattern)

        self.trans_log = os.path.join(self.config.working_folder, 'monitor.log')
        # read last transfered folder.
        if os.path.exists(self.trans_log):
            f = open(self.trans_log)
            for line in f:
                if line:
                    self.last_trans_folder = line.strip()
            f.close()
            self.logger.message("recorded last trans folder: %s"%self.last_trans_folder)
        pass
  
    def start(self):
        """
        start the monitoring.
        """
        self.logger.message("monitoring is on.")
        self.monitoring = True
        if self.thread == None:
            self.thread = self.MonitoringThread(self)
        self.thread.start()
        pass
    
    def stop(self):
        """
        request to stop the monitoring.
        """
        self.logger.message("stop monitoring...")
        self.monitoring = False
        pass

    def log_last_folder(self):
        f = open(self.trans_log, 'w+')
        f.write('\n%s'%self.last_trans_folder)
        f.close()
   
    def launch_trans(self, folder):
        from ez_trans import engine

        self.logger.message("launch trans jobs for folder %s" %folder)

        self.last_trans_folder = folder

        for item in self.config.trans_items:
            engine_instance = engine.engine(self.config)
            engine_instance.do_transfer(folder, item.relative_path, item.zip_name, item.volume_size)

    def get_latest_folder(self):
        """
        check and get folder matching pattern with lastest modification time.
        """
        folders = glob.glob(self.pattern)
        folders = sort_by_time(folders)
        folders.sort(reverse=True)
        folder = folders[0] if len(folders) > 0 else None
        self.logger.message("latest folder:%s"%folder)
        return folder

    class MonitoringThread(threading.Thread):
        """
        A thread monitoring the folder's presence which matches the predefined pattern.
        """

        def __init__(self, owner):
            threading.Thread.__init__(self)
            self.owner = owner
            self.logger = self.owner.logger
            pass

        def run(self):
            """
            Thread run method.
            """

            self.logger.message("monitoring thread begins running...")

            now = datetime.datetime.now()
            hour = now.hour

            while self.owner.monitoring:
                if hour >= self.owner.config.start_hour and hour <= self.owner.config.end_hour :
                    self.logger.message("current hour: %d in range(%d-%d), checking..."
                                        %(hour,self.owner.config.start_hour,
                                        self.owner.config.end_hour))
                    latest_folder = self.owner.get_latest_folder()

                    if latest_folder and not latest_folder == self.owner.last_trans_folder:
                        self.owner.last_trans_folder = latest_folder
                        self.owner.log_last_folder()

                        # wait till indicator file/folder presents
                        if self.owner.config.readyindicator:
                            indicator = os.path.join(latest_folder, self.owner.config.readyindicator)
                            passed_time = 0
                            while(True):
                                if (os.path.exists(indicator)):
                                    break
                                else:
                                    self.logger.message('ready indicator not presents - %s'%indicator)
                                    self.logger.message('trying to detect in 30 seconds')
                                    time.sleep(1*30)
                                    passed_time += 30
                                    if self.config.time_out and self.config.time_out > 0:
                                        if passed_time > self.config.time_out:
                                            self.logger.error("failed due to time out!")
                                            continue

                        if (self.owner.config.delay_before_trans != None):
                            self.logger.message("wait %s till launch transfer as defined" %self.owner.config.delay_before_trans)
                            time.sleep(self.owner.config.delay_before_trans)

                        self.owner.launch_trans(latest_folder)

                        self.logger.message('Transfer job is done.')
                    else:
                        self.logger.message('latest folder is already transfered - %s' 
                                            % self.owner.last_trans_folder)
   

                else:
                    self.logger.message ('current hour: %d' % hour)
                    self.logger.message (' not in range [%d-%d]'%(self.owner.config.start_hour, self.owner.config.end_hour))
                self.logger.message('try check again in 5 minutes')
                time.sleep(5*60) # 5 minutes till next check

            self.logger.message ('monitoring thread ends!')
            self.owner.thread = None


    




    

