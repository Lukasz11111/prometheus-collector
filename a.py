# import subprocess
# from subprocess import PIPE, Popen

# # a=subprocess.run("sudo docker  exec -it  revdebug-devops-1 netstat -tn | grep 42734 | grep ESTABLISHED | wc -l", shell=True, check=True)
# # subprocess.run("sudo docker  cp /bin/netstat revdebug-devops-1:/bin/netstat", shell=True, check=True)



# # print(dir(a))
# # print(a.stdout)

# command = "sudo docker  exec -it  revdebug-devops-1 netstat -tn | grep 42734 | grep ESTABLISHED | wc -l"
# process = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
# output, error = process.communicate()

# print(output.decode("utf-8"))

# import psutil
# import time
# # print(dir(psutil))

# # print(psutil.net_if_addrs())
# # print(" ")
# # print(psutil.net_if_stats())
# # print(" ")
# while True:
#     print(psutil.net_io_counters())
#     time.sleep(3)

# # print(" ")
# # # print(psutil.net_connections())
# import pyshark

# # def get_packet_info(interface=None):
# #     """
# #     Returns the size of the transmitted data using Wireshark.

# #     Args:
# #         interface: A string. Name of the interface to sniff on.

# #     Returns: Size of the packet sent over WebSockets in a given event.
# #     """
# #     if interface is None:
# #         raise Exception("Please provide the interface used.")
# #     else:
# #         capture = pyshark.LiveCapture(interface=interface)
# #         capture.sniff(timeout=60)
# #         for packet in capture:
# #             try:
# #                 packet_info = packet.pretty_print()
# #             except:
# #                 raise Exception("Cannot determine packet info.")
# #         return packet_infopip


# capture = pyshark.LiveCapture(interface='wlan0')
# print(capture)

# import time
# import psutil

# def main():
#     old_value = 0    

#     while True:
#         new_value = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv

#         if old_value:
#             send_stat(new_value - old_value)

#         old_value = new_value

#         time.sleep(10)

# def convert_to_gbit(value):
#     return value/1024./1024./1024.*8

# def send_stat(value):
#     print ("%0.3f" % convert_to_gbit(value))

# main()
import time
import psutil

while True:
    new_value_send = psutil.net_io_counters().bytes_sent
    new_value_recv = psutil.net_io_counters().bytes_recv

    print(f"Send: {new_value_send}  Recv: {new_value_recv}")
    time.sleep(5)