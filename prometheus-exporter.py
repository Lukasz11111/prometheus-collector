from prometheus_client import  Gauge, push_to_gateway, CollectorRegistry
import os
import time
import psutil


minCpu=os.getenv("MIN_MEM_VALUE")
minMem=os.getenv("MIN_CPU_VALUE")

# minCpu=1
# minMem=1
instanceName=os.getenv("INSTANCE_NAME")
jobName=os.getenv("JOB_NAME")

cpu_count=len(psutil.Process().cpu_affinity())


def getCpuStats():
    return psutil.cpu_percent(interval=None)

def getFreeDiskSpacePercent(path):
    return psutil.disk_usage(path).percent

def getFreeDiskSpacePercentLambdaFactory(path):
    return lambda: getFreeDiskSpacePercent(path)

def getMemoryUsage():
    return psutil.virtual_memory().percent

def getSingleProcessCpuStats(proc):
    return proc.cpu_percent(interval=None)

def gettSingleProcessMemoryUsage(proc):
    return proc.memory_percent()

def getSingleProcessCpuStatsFactory(proc):
    return lambda: getSingleProcessCpuStats(proc)

def gettSingleProcessMemoryUsageFactory(proc):
    return lambda: gettSingleProcessMemoryUsage(proc)



def main(registry):
    # saveDps(registry)
    cpuUsage_all = Gauge('cpu_usage_all', 'Usage of the CPU in percent', ["instance"],registry=registry)
    cpuUsage_all.labels(instanceName).set(psutil.cpu_percent(interval=None))

    memoryGauge_all = Gauge('memmory_usage_all', 'Usage of memory in percent',["instance"], registry=registry)
    memoryGauge_all.labels(instanceName).set(psutil.virtual_memory().percent)
    singleProcess(registry)


def saveDps(registry):
    dps = psutil.disk_partitions()
    for partition in dps:
        print('used_disk_space'+partition.mountpoint.replace('/', '_').replace('.', '_') )
        g = Gauge('used_disk_space'+partition.mountpoint.replace('/', '_').replace('.', '_').replace('-', '_'), 'Used disk space in percent', registry=registry)
        g.set_function(getFreeDiskSpacePercentLambdaFactory(partition.mountpoint)) 


def saveMem(proc,memoryGauge):

    r=proc.memory_percent()
    if float(r)>float(minMem):
        memoryGauge.labels(proc.name(), proc.pid,instanceName).set(r)
    

def saveCPU(proc,cpuUsage):

    r=proc.cpu_percent(interval=None)/cpu_count
    if float(r)>float(minCpu):

        cpuUsage.labels(proc.name(), proc.pid,instanceName).set(r)


        

def singleProcess(registry):
    memoryGauge = Gauge('memmory_usage', 'Usage of memory in percent', ["Name", "PID","instance"] ,registry=registry)
    cpuUsage = Gauge('cpu_usage', 'Usage of the CPU in percent', ["Name", "PID", "instance"], registry=registry)
    for proc in psutil.process_iter():
        saveCPU(proc,cpuUsage)
        saveMem(proc,memoryGauge)


while True:
    registry = CollectorRegistry()
    # g = Gauge('job_last_success_unixtime', 'Last time a batch job successfully finished', registry=registry)
    main(registry)
    
    push_to_gateway('3.127.247.150:9091', job=jobName, registry=registry)
    # print("push")

    time.sleep(15)
# for proc in psutil.process_iter():

#     if proc.cpu_percent(interval=None)>0:
#         print(f"{proc.name()} cpu: {proc.cpu_percent()}  mem: {proc.memory_percent()} ",flush=True)



# p = psutil.Process(3198914)

# print(p.cpu_percent(),flush=True)



# p = psutil.Process(pid=3198914)

# print(p.cpu_percent(interval=10))
# print(p.cpu_percent(interval=None))
# print(p.name())

# time.sleep(10)

# print(p.cpu_percent(interval=None))
# for i in range(100):
#     usage = p.cpu_percent(interval=None, percpu=False)
#     print(usage)
    # do other things

# cpu = psutil.cpu_times_percent(interval=0.4, percpu=False)
# print(cpu)
# print(psutil.cpu_percent(),flush=True)

# p = psutil.Process()
# with p.oneshot():
#     p.name()  # execute internal routine once collecting multiple info
#     p.cpu_times()  # return cached value
#     p.cpu_percent()  # return cached value
#     p.create_time()  # return cached value
#     p.ppid()  # return cached value
#     p.status()  # return cached value
#     print(p.cpu_percent(),flush=True)

# print(dir( psutil),flush=True)
# print(dir( psutil),flush=True)
    # time.sleep(15)



    