import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


f = open('dashboard.json',encoding='utf-8')
data = json.load(f)
f.close()

instanceName=str(os.getenv("INSTANCE_NAME"))
dashboardName=os.getenv("GRAFANA_DASHBOARD")
authorization=os.getenv("GRAFANA_API_KEY")


if dashboardName:
    data['dashboard']['title']=dashboardName
else:
    print("Set GRAFANA_DASHBOARD in .env file")
    exit()


for panel in data['dashboard']['panels'][1:]:
    panel["targets"][0]["expr"]=str(panel["targets"][0]["expr"]).replace("MyInstance",instanceName)




headers = {'Content-type': 'application/json', 'Accept': 'application/json',"Authorization": authorization}
r= requests.post(url="http://18.193.73.140:3000/api/dashboards/db",  data=json.dumps(data,ensure_ascii=False) , headers=headers)
