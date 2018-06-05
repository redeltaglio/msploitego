from pprint import pprint
import re
from datetime import datetime
from common.MaltegoTransform import *
from common.postgresdb import MsploitPostgres
import sys
from common.servicefactory import getserviceentity, getosentity

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
    ip = mt.getValue()
    mac = mt.getVar("mac")
    machinename = mt.getVar("name")
    os_family = mt.getVar("os_family")
    os_name = mt.getVar("os_name")
    os_sp = mt.getVar("os_sp")
    hostid = mt.getVar("id")
    db = mt.getVar("db")
    user = mt.getVar("user")
    password = mt.getVar("password").replace("\\", "")
    mpost = MsploitPostgres(user, password, db)
    for service in mpost.getforHost(ip, "services"):
        entityname = getserviceentity(service)
        hostservice = mt.addEntity(entityname, "{}/{}:{}".format(service.get("name"), service.get("port"), hostid))
        hostservice.setValue("{}/{}:{}".format(service.get("name"), service.get("port"), hostid))
        hostservice.addAdditionalFields("ip", "IP Address", True, ip)
        for k,v in service.items():
            if isinstance(v,datetime):
                hostservice.addAdditionalFields(k, k.capitalize(), False, "{}/{}/{}".format(v.day,v.month,v.year))
            elif v and str(v).strip():
                hostservice.addAdditionalFields(k, k.capitalize(), False, str(v))
        hostservice.addAdditionalFields("user", "User", False, user)
        hostservice.addAdditionalFields("password", "Password", False, password)
        hostservice.addAdditionalFields("db", "db", False, db)
    if mac:
        macentity = mt.addEntity("maltego.MacAddress", mac)
        macentity.setValue(mac)
        macentity.addAdditionalFields("ip", "IP Address", True, ip)
    if machinename and re.match("^[a-zA-z]+", machinename):
        hostentity = mt.addEntity("msploitego.Hostname", machinename)
        hostentity.setValue(machinename)
        hostentity.addAdditionalFields("ip", "IP Address", True, ip)
    osentityname, osdescription = getosentity(os_family,os_name)
    if os_sp:
        osdescription += " {}".format(os_sp)
    osentity = mt.addEntity(osentityname, osdescription)
    osentity.setValue(osdescription)
    osentity.addAdditionalFields("ip", "IP Address", True, ip)

    mt.returnOutput()
    mt.addUIMessage("completed!")

dotransform(sys.argv)
# args = ['postgresservices.py',
#  '10.11.1.10',
#  'ipv4-address=10.11.1.10#ipaddress.internal=false#updated_at=23/1/2018#vuln_count=8#exploit_attempt_count=6#id=531#state=alive#os_family=Windows#os_name=Windows 2003#workspace_id=18#note_count=9#mac=00:50:56:B8:76:82#service_count=2#purpose=server#address=10.11.1.10#os_sp=SP2#name=10.11.1.10#created_at=23/1/2018#user=msf#password=unDwIR39HP8LMSz3KKQMCNYrcvvtCK478l2qhIi7nsE\\\\\\=#db=msf']
#
# dotransform(args)