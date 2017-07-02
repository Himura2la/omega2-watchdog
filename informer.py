from time import localtime, strftime

class Informer(object):
    def __init__(self, module=''):
        self.module = module

    def _add_meta_info(self, level, msg):
        msg_type = '%s>%s' % (level, self.module) if self.module else level
        return "[%s|%s] %s" % (msg_type, strftime("%d.%m|%H:%M:%S", localtime()), msg)

    @property
    def _log_path(self):
        base_path = '/root/watchdog/logs'
        return '%s/%s.log' % (base_path, strftime("%m_%d", localtime()))

    def log(self, msg):
        print(msg)
        with open(self._log_path, 'a') as f:
            f.write(msg + '\n')

    def ok(self, what):
        print(self._add_meta_info('INFO', what + ' works'))

    def info(self, msg):
        self.log(self._add_meta_info('INFO', msg))

    def notice(self, msg):
        self.log(self._add_meta_info('NOTICE', msg))

    def warning(self, msg):
        self.log(self._add_meta_info('! WARNING', msg))

    def crytical(self, msg):
        self.log(self._add_meta_info('!!! CRYTICAL', msg))
