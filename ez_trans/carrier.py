'''
Created on Mar 06, 2013

'''

import socket
import ftplib
from ftplib import FTP
import queue, threading, time, os

from ez_trans import logger
from ez_trans.config import *

class carrier(object):
    """carrier to do the file transfer job."""

    def __init__(self):
        pass

class ftp_carrier(carrier):

    port = ftplib.FTP_PORT

    log = logger.SimpleLogger()
    
    ''' And FTP Wrapper class.    
    Encapsulate the general FTP operations like upload a bunch of files.        
    '''
    def __init__(self, server, user = None, password = '', port = ftplib.FTP_PORT):
        '''
        carrier to upload files via FTP.
        '''
        carrier.__init__(self)

        self.server = server
        self.user = user
        self.password = password
        if port:
            self.port = port
        self.log.message ("ctor %s"%self)
        pass
    def __str__(self):
        str = "%s - server:%s;user:%s"%(self.__class__,self.server, self.user)
        return str

    def open_connection(self):
        try:
            ftp = FTP()
            ftp.connect(self.server, self.port)
            ftp.login(self.user, self.password)
        except ftplib.Error as e:
            self.log.error("failed to open connection, e.no=%d; e=%s"%(e.errno,e))
        except ConnectionRefusedError as e:
            self.log.error("connection refused! e=%s" %e)
            ftp = None
        return ftp
        
    def upload(self, files, ftpfolder, max_threads = 21):
        ''' Upload a bunch of files to specific folder on the FTP server, args:
        - files: a list of files to be uploaded.
        - ftpfolder: the folder on FTP server where the files to be stored. 
        '''
        self.log.message ('upload to %s for files %s' %(ftpfolder, files))
        
        self.ftpfolder = ftpfolder
        # make sure the target directory exists in FTP server
        try:
            ftp = self.open_connection()        
        except socket.gaierror as e:
            self.log.error ('server is unavailable, e=%s' %e)
            raise           
        except ftplib.all_errors as e:
            self.log.error ('general ftp error %s' % e)
            raise

        if not ftp:
            self.log.error("cannot connect to ftp.")
            return False
        
        try:
            ftp.mkd(self.ftpfolder)
        except ftplib.error_perm as e:
            self.log.warn ('the folder already exist. %s' % e)
        ftp.close()
            
        q = queue.Queue()
        for file in files:
            q.put(file) 

        self.threads = []

        num_threads = min(len(files), max_threads)
        
        for i in range(num_threads):
            thread = FTPThread(self, q)
            self.threads.append(thread)
            thread.daemon = True
            thread.start()
        pass
        q.join()
      
        self.log.message ("All done, congratulations!")
        return True
        
    def upload_one(self, filepath):
        ftp = FTP(self.server, self.user, self.password)
        
        ftp.cwd(self.ftpfolder)
        
        parts = os.path.split(filepath)
        self.log.message ('begin uploading...%s' % parts[1])

        try:              
            ftp.storbinary('STOR ' + parts[1], open(filepath, 'rb'))
        except IOError as e:
            self.log.message ('IO error in uploading %s'%e)
            pass
        except ftplib.error_perm as e:
            self.log.error('Permission error %s' %(e))
            pass
        finally:
            ftp.close()
        self.log.message ("transfer succeeded for %s" %filepath)
 
        pass             
      
    
class FTPThread(threading.Thread):
    def __init__(self, carrier, q):
        threading.Thread.__init__(self)
        self.carrier = carrier
        self.q = q

        self.daemon = True
        
    def run(self):
        while True:
            file_path = self.q.get()
            if file_path:
                self.carrier.upload_one(file_path)        
                self.q.task_done()
            else:
                break                           
            pass
    
    
        
        
        