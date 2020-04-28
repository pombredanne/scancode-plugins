#!/usr/bin/env python
# In case of any issue please write chamohan@amd.com

import json
import sys

filename = sys.argv[1]

with open(filename) as f:
  data = json.load(f)
modifications_counter = 0
for i in data['files']:
   if i['licenses'] is None:
      print("NoLicence")
   else:
     for j in i['licenses']:
        try:
           if j['score'] != 100.0:
              print(j['score'])
              print(i['path'])
              print(i['licenses'])
              print(i['licence_modifications'])
              modifications_counter = modifications_counter + 1
        except Exception:
           pass


if modifications_counter > 0:
    print("Failed")
    sys.exit(1)
else:
    print("Tests Passed")
