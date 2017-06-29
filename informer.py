from time import localtime, strftime

class Informer(object):
    def __init__(self, module=''):
        self.module = module

    def _add_meta_info(self, level, msg):
        msg_type = '[%s>%s]' % (level, self.module) if self.module else'[%s]' % level
        return "[%s|%s] %s" % (strftime("%d.%m %H:%M:%S", localtime()), msg_type, msg)

    def info(self, msg):
        msg = self._add_meta_info('INFO', msg)
        print(msg)

    def notice(self, msg):
        msg = self._add_meta_info('NOTICE', msg)
        print(msg)

    def warning(self, msg):
        msg = self._add_meta_info('! WARNING !', msg)
        print(msg)

    def crytical(self, msg):
        msg = self._add_meta_info('!!! CRYTICAL !!!', msg)
        print(msg)