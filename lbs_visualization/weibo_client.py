# coding = utf-8
from gearman import GearmanClient
import json
  
new_client = GearmanClient(['192.168.5.41:4730'])
attr = dict(dist=20, center={'lng': 121.435101153, 'lat': 31.1952376167}, time_start=1385740800, time_end=1405995856)
a = json.dumps(attr)

current_request = new_client.submit_job('user_lbs', a)
new_result = current_request.result
print new_result