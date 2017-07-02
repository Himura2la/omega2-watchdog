#!/bin/sh

cp rebooter.procd /etc/init.d/rebooter
chmod +x /etc/init.d/rebooter
/etc/init.d/rebooter enable
echo [INFO] Checking symlink...
ls -lh /etc/rc.d | grep rebooter
/etc/init.d/rebooter enabled && echo Service is ready!