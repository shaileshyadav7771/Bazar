import logging
import argparse
import json
import os
import requests
from collections import OrderedDict
from kubernetes import client, config
import yaml
# import recertifi
def main(namespace='data-neutron-prod', remote_cluster=False):
    logger = logging.getLogger()
    # TODO: we should allow configuration of the log level through a flag
    # logger.setLevel(logging.DEBUG)
    print('10')
    if bool(remote_cluster):
        config.load_kube_config("{}/.kube/config".format(os.environ["HOME"]))
        print('Config:',config)
    else:
        config.load_incluster_config()
        print('Config:', config)
    logging.info("forwarding pod stats")
    get_deploys(namespace)
    get_configs(namespace)
def get_deploys(namespace):
    finalJson = {}
    flag = 0
    finalArr = []
    app_list=[line.strip() for line in open('apps.properties')]
    headers = {
        "Content-Type": "application/json"
    }
    v1 = client.AppsV1Api()
    deploys = v1.list_namespaced_deployment(namespace, watch=False)
    for d in deploys.items:
        if any(s in d.metadata.name for s in app_list):
            name = d.metadata.name
            namepsace = d.metadata.namespace
            replicas = str(d.spec.replicas)
            available_replicas = str(d.status.available_replicas)
            ready_replicas = str(d.status.ready_replicas)
            containers = ""
            con = str(len(d.spec.template.spec.containers))
            requestCPU = "0" if (d.spec.template.spec.containers[0].resources.requests is None or ("cpu" not in d.spec.template.spec.containers[0].resources.requests)) else d.spec.template.spec.containers[0].resources.requests['cpu']
            requestMemory = "0" if (d.spec.template.spec.containers[0].resources.requests is None or ("memory" not in d.spec.template.spec.containers[0].resources.requests)) else d.spec.template.spec.containers[0].resources.requests['memory']
            limitsCPU = "0" if (d.spec.template.spec.containers[0].resources.limits is None or ("cpu" not in d.spec.template.spec.containers[0].resources.limits)) else d.spec.template.spec.containers[0].resources.limits['cpu']
            limitsMemory = "0" if (d.spec.template.spec.containers[0].resources.limits is None or ("memory" not in d.spec.template.spec.containers[0].resources.limits)) else d.spec.template.spec.containers[0].resources.limits['memory']
            for c in d.spec.template.spec.containers:
                containers += ","+c.image.replace("docker.apple.com/","")
            finalArr.append(get_json_dict(name ,namespace,replicas,con,containers,requestCPU,requestMemory,limitsCPU,limitsMemory,available_replicas,ready_replicas))
            flag = flag + 1
            if flag == 20:
                finalJson["items"]=finalArr
                postJson = json.dumps(finalJson)
                #print (postJson)
                r = requests.post(os.environ['STARGAZE_URL']+"/api/post_to_db", data=postJson,auth=('starbot', 'starpass'),verify=True,headers=headers)
                print (r.status_code)
                flag = 0
                finalArr = []
    finalJson["items"]=finalArr
    postJson = json.dumps(finalJson)
    #print(postJson)
    r = requests.post(os.environ['STARGAZE_URL']+"/api/post_to_db", data=postJson,auth=('starbot', 'starpass'),verify=True,headers=headers)
    print (r.status_code)
    if len(deploys.items) == 0:
        logging.debug('no deploys found. skipping.')
        return
def get_configs(namespace):
    finalJson = {}
    flag = 0
    finalArr = []
    app_list=[line.strip() for line in open('apps.properties')]
    headers = {
        "Content-Type": "application/json"
    }
    v1 = client.CoreV1Api()
    deploys = v1.list_namespaced_config_map(namespace, watch=False)
    env=['dev','ci','staging','prod','kh-beta','kh-staging','kh-sig']
    for d in deploys.items:
        if  (any([s in d.metadata.name for s in app_list]) and any([ d.metadata.name.endswith(e) or d.metadata.name.endswith('config') for e in env for s in app_list])):
            finalJson['geonode']=json.dumps(yaml.load(d.data['geonode.json']))
            finalJson['name']=d.metadata.name.replace('-config','')
            postJson=json.dumps(finalJson)
            #print (postJson)
            r = requests.post(os.environ['STARGAZE_URL']+"/api/post_k8s_configs", data=postJson,auth=('starbot','starpass'),verify=True,headers=headers)
            print(r.status_code)
    if len(deploys.items) == 0:
        logging.debug('no configs found. skipping.')
        return
def get_json_dict(name ,namespace,replicas,con,containers,requestCPU,requestMemory,limitsCPU,limitsMemory,available_replicas,ready_replicas):
    jsonDict = {
    "app" : name,
    "namespace" : namespace,
    "replicas" : replicas,
    "container_count" : con,
    "container_images" : containers,
    "request_cpu" : requestCPU,
    "request_memory" : requestMemory,
    "limits_cpu" : limitsCPU,
    "limits_memory" : limitsMemory,
    "available_replicas" : available_replicas,
    "ready_replicas" : ready_replicas
     }
    return jsonDict

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='hubble exporter for k8s')
    parser.add_argument('--namespace', type=str, required=False, default='data-neutron-prod',
                        help='Name of the namespace ')
    parser.add_argument('--remote-cluster', type=lambda x: (str(x).lower() == 'true'),
                        required=False, default=False, help='connect to remote cluster')
    return parser.parse_known_args()[0]
if __name__ == '__main__':
    args = parse_args()
    main(
        namespace=args.namespace,
        remote_cluster=args.remote_cluster
    )
















# def decor(func):
#     def inner(name):
#         names=['CM','PM']
#         if name in names:
#             print("VIP")
#         else:
#             func(name)
#     return inner
#
# @decor
# def guest(name):
#     print('normal user:',name)
#
# guest('CM')
# guest('SDGHG')
#
# range(10)
# 0 10-1 9 1
































































# key={}
# key[1] = 34
# key[2] = 7
# key[3] = 9
# key[4] = 87
#
#
# d=list(key.values())
#
# print(d)  #[34, 7, 9, 87]
#
# small_num=7
# list=[]
# i=0
# for x in d:
# 	if x[i] < x[i+1]:
# 		x[i]=x
# 		x.append(x[i])
# 	else:
# 		i=i+1


#
# def addToList(val, list=[]):
# 	list.append(val)
# 	return list
#
# list1 = addToList(1)
#
# list2 = addToList(123,[])
#
# list3 = addToList('a’)
#
#
#
# print ("list1 = %s" % list1)
#
# print ("list2 = %s" % list2)
#
# print ("list3 = %s" % list3)
#
#
# def m1
#

#
# class A:
# def xyz(self):
#
#  print('abc')
#
# def xyz(self,i):
#
#  print('second')
#
# ob =A()
#
# ob.xyz()
#
#
# class Parent(object):
# 	x = 1
#
#
# class Child1(Parent):
# 	pass
#
#
# class Child2(Parent):
# 	pass
#
#
# print(Parent.x, Child1.x, Child2.x)
# Child1.x = 2
# print(Parent.x, Child1.x, Child2.x)
# Parent.x = 3
# print(Parent.x, Child1.x, Child2.x)


# import re
#
#
# s=re.search("12may2021",'shailesg12may2021')
# print(s)

#view.py
#
# def hello_world(request):
#
# 	return render('app/.html')





#[25,30,55,78,50,32,21]
#
# i=0
# def check_list(list):
# 	x=list
# 	if x[i] < x[] < x[2]:
# 		if x[4] > x[5] > x[6]:
# 			print('The given list is Pyramid')
# 		else:
# 			print("No")
#
#
#
# check_list([25,30,55,78,50,32,21])
#
# max=10
#
#
























