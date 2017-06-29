import subprocess

class Tester(object):
    def __init__(self, server_obj, verbose=False):
        self.verbose = verbose
        self.s = server_obj

    def _call(self, cmd):
        try:
            if self.verbose:
                print('[CALL] ' + cmd)
            ret = str(subprocess.check_output(cmd, shell=True))
            return bool(ret.split("packets transmitted,", 1)[-1].split(" received,", 1)[0])
        except subprocess.CalledProcessError:
            return False

    def ping(self, host, waiting_time):
        return self._call(' '.join(["ping", host, "-c", "1", "-W", str(waiting_time)]))

    def remote_ping(self, host, waiting_time):
        return self._call(' '.join([self.s.remote_run_path, "ping", host,
                                    "-c", "1", "-W", str(waiting_time)]))
