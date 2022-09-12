import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

instanceName=str(os.getenv("INSTANCE_NAME"))
dashboardName=os.getenv("GRAFANA_DASHBOARD_NAME")
dashboardPanel=os.getenv("GRAFANA_DASHBOARD_PANEL")
authorization=os.getenv("GRAFANA_API_KEY")

grafanHost=os.getenv("GRAFANA_HOST")
grafanUID=os.getenv("GRAFANA_DASHBOARD_UID")
rdbPanel=os.getenv("GRAFAMA_RDB_PANEL")


headers = {'Content-type': 'application/json', 'Accept': 'application/json',"Authorization": authorization}

r= requests.get(url=f"http://{grafanHost}/api/dashboards/uid/{grafanUID}" , headers=headers)
data = r.json()


f = open('dashboard.json',encoding='utf-8')
panels = json.load(f)['dashboard']


if dashboardPanel:
    panels["panels"][0]["title"]=dashboardPanel
else:
    panels["panels"][0]["title"]="Panel"

if int(rdbPanel)==0:

    panels["panels"].pop(1)
    panels["panels"].pop(1)
    

for panel in panels['panels'][1:]:
    panel["targets"][0]["expr"]=str(panel["targets"][0]["expr"]).replace("MyInstance",instanceName)
    panel["title"]=f'{panel["title"]} - {instanceName}'
# print(panels['panels'][0]['panels'])

# print(data['dashboard']['panels'])
for panel in panels['panels']:
    data['dashboard']['panels'].append(panel)


data["overwrite"]=True



headers = {'Content-type': 'application/json', 'Accept': 'application/json',"Authorization": authorization}
r= requests.post(url=f"http://{grafanHost}/api/dashboards/db",  data=json.dumps(data,ensure_ascii=False) , headers=headers)

print(r)
print(r.text)
print(r.status_code)

# if dashboardName:
#     data['dashboard']['title']=dashboardName
# else:
#     print("Set GRAFANA_DASHBOARD in .env file")
#     exit()

# if dashboardPanel:
#     data['dashboard']['panels'][0]["title"]=dashboardPanel
# else:
#     data['dashboard']['panels'][0]["title"]="Panel"




# for panel in data['dashboard']['panels'][1:]:
#     panel["targets"][0]["expr"]=str(panel["targets"][0]["expr"]).replace("MyInstance",instanceName)




# headers = {'Content-type': 'application/json', 'Accept': 'application/json',"Authorization": authorization}
# r= requests.post(url="http://18.193.73.140:3000/api/dashboards/db",  data=json.dumps(data,ensure_ascii=False) , headers=headers)
