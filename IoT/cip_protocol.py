import time

from cpppo.server.enip.client import connector
from cpppo.server.enip.get_attribute import attribute_operations

host = "172.19.16.185"  # Your MicroLogix IP address
send_path = ''
route_path = False
attributes = [('@1/1/1','INT')]
timeout = 1.0
depth = 1
multiple = 0

with connector(host=host) as connection:
    operations = attribute_operations(attributes, send_path=send_path, route_path=route_path)
    for idx, dsc, op, rpy, sts, val in connection.pipeline(
            operations=operations, depth=depth, multiple=multiple, timeout=timeout):
        print("%s: %3d: (%-8s) %s == %s" % (time.ctime(), idx, sts if sts else "OK", dsc, val))
