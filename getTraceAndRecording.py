
from socket import timeout
import requests
import time
import psycopg2
import json

import docker
client = docker.from_env()

global pg_ip
global os_ip
global conn

pg_ip="127.0.0.1"
os_ip="127.0.0.1"

global rdbErr
rdbErr=0


from subprocess import PIPE, Popen

def getSizeRDB(directory):
    command = f"sudo df  --output=used {directory}"
    process = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    output, error = process.communicate()

    s=str(output.decode("utf-8"))
    s = s.split("\n",2)
    return s[1]

def getContainersIP():
    global pg_ip
    global os_ip
    for x in client.containers.list():
        if 'opensearch' in str(x.name):
            os_ip =x.attrs['NetworkSettings']['Networks'][list(x.attrs['NetworkSettings']['Networks'].keys())[0]]['IPAddress']
        if 'postgres' in str(x.name):
            pg_ip=x.attrs['NetworkSettings']['Networks'][list(x.attrs['NetworkSettings']['Networks'].keys())[0]]['IPAddress']


def getTraceCount():
    r= requests.get(f"http://{os_ip}:9200/segment/_count", timeout=3)
    json_data = json.loads(r.text)
    return json_data["count"]


def connectToPG():
    global pg_ip
    global conn
    conn = psycopg2.connect(f"dbname='revdebug_db' user='rdb_user' host='{pg_ip}' password='masterkey'  connect_timeout=3")


def queryPg():
    global conn
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM public."Recordings"')
    # cur.execute("SELECT reltuples AS estimate FROM pg_class WHERE relname = 'Recordings';")
    result = cur.fetchall()
    return result
   
def connAll():  
    getContainersIP()          
    connectToPG()

try:
    connAll()
except:
    pass


def main():
    global rdbErr
    result={"trace":"","recording":"","size":""}
    try:
        result["trace"]=getTraceCount()
        result["recording"]=queryPg()[0][0]
        result["size"]=getSizeRDB("/var/revdebug/server/repo")
    except Exception as e:
        print(rdbErr)
        if rdbErr>3:
            try:
                connAll()
            except Exception as a:
                print(a)
            print(e)
            rdbErr=0
        rdbErr=rdbErr+1
    return result
        

