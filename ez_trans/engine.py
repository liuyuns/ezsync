
import glob, os

from ez_trans import compress, carrier, config, logger

class engine(object):
    """work engine in charge of compressing and transfer files"""

    log = logger.SimpleLogger()

    def __init__(self, config, log=None):
        self.config = config
        if log:
            self.log = log

    def do_transfer(self, folder, relpath, zip_name, volume_size):
        """
        doing the job to compress and then transfer.
        """
        #
        # Compress
        # 
        relative_path = os.path.relpath(folder, self.config.base_dir)
        source = os.path.join(folder, relpath)
        work_folder = os.path.join(self.config.working_folder, relative_path, self.config.key)
        zip_file = os.path.join(work_folder, zip_name)

        zipper = compress.compresser_7z(self.config)
        result = zipper.compress(folder, relpath, zip_file, volume_size)
        if not result:
            self.log.error("failed to create compress file, please check logs!")
            return False

        zip_files = glob.glob(zipper.zip_file + '*')
        self.log.message("zip files created: %s" %zip_files)
        
        #
        # Copy or FTP? FTP only now
        pass

        #
        # transfer the compressed files by FTP
        #
        target = self.config.trans_target
        transfer = carrier.ftp_carrier(target.server, target.user, target.password, target.port)
        ftp_folder = os.path.join(self.config.trans_target.relative_path, relative_path)
        result = transfer.upload(zip_files, ftp_folder)
        
        #
        if result:
            self.log.message ('upload done. clean up zip files %s' % zip_files)
            # if delete compressed file on server
            try:
                for zip in zip_files:
                    os.remove(zip)
                    pass
            except Exception as e:
                self.log.error('error in cleanup. e=%s'%e)
            pass
        else:
            self.log.error("upload failed! please check target and permission")
            return False

        return True







