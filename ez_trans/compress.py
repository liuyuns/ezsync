import os, sys, subprocess, traceback, glob
from ez_trans import logger



class compresser(object):
    log = logger.SimpleLogger()
    from ez_trans.config import config
    def __init__(self, config, log=None):
        self._config = config
        if log:
            self.log = log
        pass

    def compress(self):
        pass

class none_compresser(compresser):
    def __init__(self, config): 
        compresser.__init__(self, config)
        pass

    def compress(self):
        compresser.compress(self)

class compresser_7z(compresser):
    status = None

    def __init__(self, config, log=None):
        compresser.__init__(self, config, log)
        pass

    def compress(self, base_dir, compress_folder, zip_file, volume_size=None):
        """
        compress the source dir to zip file according to config
        [volumn_size]: acceptable params: 18m - 18 MB; 18k - 18 KB [b|k|m|g]; None - no volumes;
        """
        self.log.message("[entering compress]")

        self.zip_file = zip_file

        ### clear existing zip files first.
        try:
            self.log.message("cleaning up zip file before compress - %s" %self.zip_file)
            for file in glob.glob(self.zip_file + "*"):
                os.remove(file)
        except Exception as e:
            self.log.error("error in pre-cleanup zip files.e=%s"%e)

        # 7z <options> <archive_file> <files>
        #
        # 7-zip options: -mx9 means maximum compression
        arglist = ["7z.exe", "u", "-mx4"]
        if volume_size:
            arglist.append("-v%s"%volume_size)
        #if excludelistfile != None:
        #    arglist.append("-xr@" + excludelistfile)
        arglist.append(self.zip_file)
        arglist.append(compress_folder)

        self.log.message ("cmd to run: %s in directory: %s" % 
            (' '.join(arglist), base_dir))

        # run 7zip (in the directory to be compressed!)

        try:
            sp = subprocess.Popen(
                args=arglist,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=base_dir)
        except:
            self.log.error ("Error in running 7-zip subprocess. Traceback:%s" % traceback.format_exc())
            return False

        # wait for process to terminate, get stdout and stderr
        stdout, stderr = sp.communicate()

        #if stdout:
        #    self.log.message ("7-zip subprocess %s" % stdout)

        if stderr:
            self.log.error ("compress failed. Error:%s" % stderr)
            return False

        self.log.message("compress passed.")

        self.status = "pass"
        return True

