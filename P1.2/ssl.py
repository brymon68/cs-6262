#!/usr/bin/env python
import re
from subprocess import call
ipmatch = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:443$")

with open('master.txt', 'rb') as file:
  for row in file.readlines():
      if ipmatch.match(row.strip()):
          call(["echo", "|", "sudo", "openssl", "s_client", "-connect", row, "|", "grep", "Server"])
      elif "N/A" in row:
          pass
      else:
          print "Bad"
