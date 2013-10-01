#
import os, configparser

class config(object):
    key=None
    base_dir=None
    pattern=None
    user=None
    password=None
    readyindicator = 'build/pass.ini'
    delay_before_trans = 5  # seconds delay before launch the process
    time_out = 60*60   # time out in seconds
    start_hour = 0
    end_hour = 24

    trans_items = []
    trans_target = None

    zip_engine='7z'
    zip_args=''


    working_folder = os.environ.get('tmp')    
    
    def __init__(self, dict = None):
        self.base = None

        pass

    def load(self, ini_file):
        parser = configparser.RawConfigParser()
        parser.read(ini_file)

        attrs = self.__dir__()

        for attr in parser.options("basic"):            
            v = parser.get("basic", attr)
            if v and attr in attrs:
                self.__setattr__(attr, v)                
            else:
                pass

        # fix int memebers
        self.delay_before_trans = (int) (self.delay_before_trans)
        self.time_out = (int) (self.time_out)
        self.start_hour = (int) (self.start_hour)
        self.end_hour = (int) (self.end_hour)

        if parser.has_section('trans'):
            item = self.trans_item()
            item._load(parser, 'trans')
            self.trans_items.append(item)

        if parser.has_section('target'):
            target = self.ftp_target()
            target._load(parser, 'target')
            self.trans_target = target

    class trans_item(object):
        relative_path = "."
        zip_name = None
        def __init__(self, relative_path = '.', zip_name = None, volume_size = None):
            self.relative_path = relative_path
            self.zip_name = zip_name
            self.volume_size = volume_size
        def _load(self, parser, section):
            for attr in self.__dir__():
                if not attr.startswith("_"):
                    v = parser.get(section, attr)
                    if v:
                        self.__setattr__(attr, v)
            pass


    class ftp_target(object):
        server = None
        port = None
        user = None
        password = None
        relative_path = None

        def __init__(self, server = None, port = None, user = None, password = None, relative_path = '.'):
            self.server = server
            self.port = port
            self.user = user
            self.password = password
            self.relative_path = relative_path

        def _load(self, parser, section):
            for attr in self.__dir__():
                if not attr.startswith("_"):
                    v = parser.get(section, attr) if parser.has_option(section, attr) else None
                    if v:
                        self.__setattr__(attr, v)
            pass


       
        

    
    