from pprint import pprint

from common.nsescriptlib import scriptrunner
from common.MaltegoTransform import *
from common.corelib import bucketparser

import re

__author__ = 'Marc Gurreri'
__copyright__ = 'Copyright 2018, msploitego Project'
__credits__ = []
__license__ = 'GPLv3'
__version__ = '0.1'
__maintainer__ = 'Marc Gurreri'
__email__ = 'me@me.com'
__status__ = 'Development'

def dotransform(args):
    mt = MaltegoTransform()
    # mt.debug(pprint(args))
    mt.parseArguments(args)
    ip = mt.getVar("ip")
    port = mt.getVar("port")
    hostid = mt.getVar("hostid")
    rep = scriptrunner(port, "http-sitemap-generator", ip)

    if rep.hosts[0].status == "up":
        for res in rep.hosts[0].services[0].scripts_results:
            output = res.get("output").strip().split("\n")
            regex = re.compile("^\s{4}/")
            for line in output:
                if regex.match(line):
                    webdir = mt.addEntity("maltego.WebDir", line.strip().lstrip())
                    webdir.setValue(line.strip().lstrip())
                    webdir.addAdditionalFields("ip", "IP Address", False, ip)
                    webdir.addAdditionalFields("port", "Port", False, port)
    else:
        mt.addUIMessage("host is {}!".format(rep.hosts[0].status))
    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['smbenumusers.py',
#  'smb/445:39',
#  'properties.metasploitservice=smb/445:39#info=Windows 2000 SP0 - 4 (language:English) (name:JD)#name=smb#proto=tcp#hostid=39#service.name=smb#port=80#banner=Windows 2000 SP0 - 4 (language:English) (name:JD)#properties.service= #ip=10.11.1.223#state=open#fromfile=/root/data/report_pack/msploitdb_oscp-20180325.xml']
# dotransform(args)
