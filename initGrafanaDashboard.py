import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


f = open('dashboard.json',encoding='utf-8')
data = json.load(f)
f.close()

instanceName=str(os.getenv("INSTANCE_NAME"))
dashboardName=os.getenv("GRAFANA_DASHBOARD_NAME")
dashboardPanel=os.getenv("GRAFANA_DASHBOARD_PANEL")
authorization=os.getenv("GRAFANA_API_KEY")
rdbPanel=os.getenv("GRAFAMA_RDB_PANEL")

if int(rdbPanel)==0:
    data['dashboard']["panels"].pop(1)
    data['dashboard']["panels"].pop(1)


if dashboardName:
    data['dashboard']['title']=dashboardName
else:
    print("Set GRAFANA_DASHBOARD in .env file")
    exit()

if dashboardPanel:
    data['dashboard']['panels'][0]["title"]=dashboardPanel
else:
    data['dashboard']['panels'][0]["title"]="Panel"


for panel in data['dashboard']['panels'][1:]:
    panel["targets"][0]["expr"]=str(panel["targets"][0]["expr"]).replace("MyInstance",instanceName)
    panel["title"]=f'{panel["title"]} - {instanceName}'
    



headers = {'Content-type': 'application/json', 'Accept': 'application/json',"Authorization": authorization}
r= requests.post(url="http://18.193.73.140:3000/api/dashboards/db",  data=json.dumps(data,ensure_ascii=False) , headers=headers)
