# coding=utf-8
from pymongo import MongoClient
from pytz import timezone

tz = timezone("Asia/Shanghai")
utc = timezone('UTC')
client = MongoClient('192.168.5.40', 57017, tz_aware=True)
mapreduce = client['mapreduce']

pattern = {
    "nginx": "%{IPV4:source_ip} %{DATA:phpsessid} %{DATA:urm_id} %{USERNAME:remote_user} \[%{HTTPDATE:timestamp}\] %{QS:request} %{INT:status} %{INT:body_bytes_sent} %{QS:http_referer} %{QS:http_user_agent} %{INT:request_length} %{INT:bytes_sent} %{DATA:upstream_addr} %{DATA:upstream_response_time} %{BASE10NUM:request_time}",
    'iPhone_user': "OS %{DATA:Release} .* (MicroMessenger/%{DATA:MicroMessenger})?( NetType/%{DATA:NetType})?( .*)?\"",
    'Android_user': "Android %{DATA:Release};(.*)?(MicroMessenger/%{DATA:MicroMessenger})?( NetType/%{DATA:NetType})?( .*)?\""
}