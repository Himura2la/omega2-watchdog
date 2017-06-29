import subprocess

class Server(object):
    def __init__(self, remote_run_path):
        self.remote_run_path = remote_run_path

    def soft_reboot(self):
        try:
            subprocess.call(self.remote_run_path + " sudo reboot", shell=True)
            return True
        except subprocess.CalledProcessError:
            return False
