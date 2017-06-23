#!/usr/bin/env python

import sys
sys.path.append("/pkg/bin/")
from ztp_helper import ZtpHelpers
import json, tempfile
from pprint import pprint

class ZtpFunctions(ZtpHelpers):

    def set_root_user(self):
        config = """ !
                     username netops
                     group root-lr
                     group cisco-support
                     secret 5 $1$7kTu$zjrgqbgW08vEXsYzUycXw1
                     !
                     end"""



        with tempfile.NamedTemporaryFile(delete=True) as f:
            f.write("%s" % config)
            f.flush()
            f.seek(0)
            result = self.xrapply(f.name)

        if result["status"] == "error":

            self.syslogger.info("Failed to apply root user to system %s"+json.dumps(result))

        return result





if __name__ == "__main__":

    # Create an Object of the child class, syslog parameters are optional. 
    # If nothing is specified, then logging will happen to local log rotated file.

    ztp_script = ZtpFunctions(syslog_file="/root/ztp_python.log", syslog_server="11.11.11.2", syslog_port=514)

    print "\n###### Debugs enabled ######\n"

    # Enable verbose debugging to stdout/console. By default it is off
    ztp_script.toggle_debug(1)

    # Change context to XR VRF in the linux shell when needed. Depends on when user changes config to create network namespace.

    print "\n###### Change context to user specified VRF ######\n"
    ztp_script.set_vrf("global-vrf")



    # Use the child class methods
    print "\n###### Using Child class method, setting the root user ######\n"
    ztp_script.set_root_user()


    # Use the parent class helper methods

    print "\n###### Installing k9sec package with Debugs ######\n"
    ztp_script.install_xr_package("http://11.11.11.2:9090/packages/ncs5500-k9sec-2.2.0.0-r62121I.x86_64.rpm")

    # Disable debugs
    print "\n###### Debugs Disabled ######\n"
    ztp_script.toggle_debug(0)


    print "\n###### install mgbl package without debugs ######\n"
    ztp_script.install_xr_package("http://11.11.11.2:9090/packages/ncs5500-mgbl-3.0.0.0-r62121I.x86_64.rpm")

    # Show commands using Parent class helper method: xrcmd

    print "\n###### Executing a show command ######\n"
    pprint(ztp_script.xrcmd({"exec_cmd" :  "show running-config"}))


    # Config apply with file using Parent class helper method: xrapply

    print "\n###### Apply valid configuration using a file ######\n"
    config = """ !
                 hostname customer
                 !
                 cdp
                 !
                 end"""



    with tempfile.NamedTemporaryFile(delete=True) as f:
        f.write("%s" % config)
        f.flush()
        f.seek(0)
        print ztp_script.xrapply(f.name)

    # Config apply with string using Parent class helper method: xrapply_string

    print "\n###### Apply valid configuration using a string ######\n"
    out = ztp_script.xrapply_string("hostname customer2")
    pprint(out)

    # Send syslogs to the preset syslog destinations (see above)

    print "\n###### Sending Syslogs to Server/file ######\n"
    ztp_script.syslogger.info("Hostname updated")
    ztp_script.syslogger.info(ztp_script.xrcmd({"exec_cmd" : "show running-config hostname"}))

    # Error handling

    print "\n###### Apply invalid configuration using a string ######\n"
    pprint(ztp_script.xrapply_string("hostnaime customer2"))
