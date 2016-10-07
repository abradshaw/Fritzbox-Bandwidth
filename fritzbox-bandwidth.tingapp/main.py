import tingbot
from tingbot import *
import requests
from lxml import etree
import time



# setup code here
# this query pulls back the info on the WAN connection such as speed
url = 'http://192.168.178.1:49000/igdupnp/control/WANCommonIFC1' 
headers = { 'Content-Type': 'text/xml; charset="utf-8"', 'SoapAction': 'urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1#GetAddonInfos' }
xml = """<?xml version='1.0' encoding='utf-8'?>
<s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'>
 <s:Body> <u:GetAddonInfos xmlns:u='urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1' /> </s:Body>
 </s:Envelope>"""

# this query would pull back info on the WAN connection  such as IP addrees
url2 = 'http://192.168.178.1:49000/igdupnp/control/WANIPConn1' 
headers2 = { 'Content-Type': 'text/xml; charset="utf-8"', 'SoapAction': 'urn:schemas-upnp-org:service:WANIPConnection:1#GetExternalIPAddress' }
xml2 = """<?xml version='1.0' encoding='utf-8'?>
 <s:Envelope s:encodingStyle='http://schemas.xmlsoap.org/soap/encoding/' xmlns:s='http://schemas.xmlsoap.org/soap/envelope/'>
 <s:Body> <u:GetExternalIPAddress xmlns:u='urn:schemas-upnp-org:service:WANIPConnection:1' /> </s:Body> 
 </s:Envelope>"""

def sizeof_fmt(num, suffix='b'):
    # our value comes back in bytes, lets make that into bits
    num *=8
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)



@every(seconds=1)
def loop():
    # drawing code here
    r = requests.post(url, data=xml, headers=headers)
    x = etree.fromstring(r.content)

    r2 = requests.post(url2, data=xml2, headers=headers2)
    x2 = etree.fromstring(r2.content)


    rec = x.find('*//NewByteReceiveRate').text
    rec_txt = 'Down: ' + sizeof_fmt(int(rec))
    
    send = x.find('*//NewByteSendRate').text
    send_txt = '    Up: ' + sizeof_fmt(int(send))
    
    ip = x2.find('*//NewExternalIPAddress').text
    ip_txt = "   IP: " + ip    
  
    screen.fill(color='black')
    screen.rectangle( xy=(0,0), align='topleft', size=(320,45), color=('blue') )
    
    # pop the login in the top right
    screen.image('icon.png', align='topright', scale=0.4)
    
    screen.text(ip_txt, xy=(0, 25),color='white', align='left', font_size=20)
    screen.text(rec_txt, xy=(10, 100),color='green', align='left')
    screen.text(send_txt, xy=(10, 160),color='green', align='left')

    screen.rectangle( xy=(0,240), align='bottomleft', size=(320,30), color=('blue') )
    screen.text(ip_txt, xy=(0, 25),color='white', align='left', font_size=20)
   
    date_format_str = "%d %B %Y"
    time_format_str = "%H:%M:%S"
    
    current_date = time.strftime("%d %B %Y")
    current_time = time.strftime(time_format_str)
    
    screen.text(current_time, xy=(300, 225), color='white', font_size=15, align='right')
    screen.text(current_date, xy=(20, 225), color='white', font_size=15, align='left')
    

tingbot.run()
