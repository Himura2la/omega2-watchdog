import subprocess

class DDNS(object):
    def update(self):
        return not subprocess.call("/root/rinker.sh", shell=True)
