import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()


#  "expr": "cpu_usage_all{exported_instance=\"APP-LM_test\"}",
#   "expr": "cpu_usage{exported_instance=\"APP-LM_test\"}",
#   "expr": "memmory_usage{exported_instance=\"APP-LM_test\"}", 
#   "expr": "memmory_usage_all{exported_instance=\"APP-LM_test\"}",
#  "expr": "recordingAll{exported_instance=\"Test-RDB-LM\"}",
#  "expr": "traceAll{exported_job=\"Test-RDB-LM\"}",
#  "expr": "memmory_res_usage{exported_instance=\"Test-RDB-LM\"}",
 
 
                       
instanceName=str(os.getenv("INSTANCE_NAME"))
dashboardName=os.getenv("GRAFANA_DASHBOARD_NAME")
dashboardPanel=os.getenv("GRAFANA_DASHBOARD_PANEL")
authorization=os.getenv("GRAFANA_API_KEY")

grafanHost=os.getenv("GRAFANA_HOST")
grafanUID=os.getenv("GRAFANA_DASHBOARD_UID")
rdbPanel=os.getenv("GRAFAMA_RDB_PANEL")
rdbPanelUpdate=os.getenv("GRAFANA_PANEL_UPDATE")


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
    

for panel in data['dashboard']['panels']:
    if str(rdbPanelUpdate) in panel["title"]:
        try:
            if int(rdbPanel)==0:
                if not ("Trace" in str(panel["title"]) or "Recording" in str(panel["title"])):
                    print(panel["targets"][0]["expr"])
                    print(panel["title"])
                    print(panel["targets"][0]["legendFormat"])
                    # panel["targets"][0]["legendFormat"]='"{{Name}} - {{PID}} - {{exported_job}}"'
            else:
                print(panel["targets"][0]["expr"])
                print(panel["title"])
                print(panel["targets"][0]["legendFormat"])
        except:
            print("jebło")
    # panel["targets"][0]["expr"]=str(panel["targets"][0]["expr"]).replace("MyInstance",instanceName)
    # panel["title"]=f'{panel["title"]} - {instanceName}'

for panel in panels['panels']:
    data['dashboard']['panels'].append(panel)


data["overwrite"]=True



# headers = {'Content-type': 'application/json', 'Accept': 'application/json',"Authorization": authorization}
# r= requests.post(url=f"http://{grafanHost}/api/dashboards/db",  data=json.dumps(data,ensure_ascii=False) , headers=headers)

# print(r)
# print(r.text)
# print(r.status_code)


