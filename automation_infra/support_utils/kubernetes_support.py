import time

import yaml
from kubernetes import client, config
from kubernetes.client import ApiException
from kubernetes.stream import stream


def get_kubernetes_core_api_instance():
    config.load_kube_config()
    return client.CoreV1Api()


def get_kubernetes_pod_status_api_instance():
    config.load_kube_config()
    return client.V1PodStatus()


def get_kubernetes_dep_api_instance():
    config.load_kube_config()
    return client.ExtensionsV1beta1Api()


def getRunningKubernetesPods(wait, retries):
    pods_list_data = {}
    pod = ""

    for retry in range(retries):
        try:
            time.sleep(5)
            exit_retries = True
            v1 = get_kubernetes_core_api_instance()
            print("Listing pods with their IPs:")
            ret = v1.list_namespaced_pod("default")
            for pod in ret.items:
                if pod.status.container_statuses[0].state.running:
                    pods_list_data[pod.metadata.name] = pod.status.container_statuses[0].state.running.started_at
                elif pod.status.container_statuses[0].state.terminated:
                    print(str.format("Pod {0} terminated", pod.metadata.name))
                else:
                    print(str.format("Pod {0} still not ready", pod.metadata.name))
                    exit_retries = False
            if exit_retries:
                return pods_list_data
        except AttributeError:
            print(str.format("Pod {0} still not ready", pod.metadata.name))
            time.sleep(wait)
        except TypeError as e:
            print(str.format("Pod {0} get status type error exception: {1} \nStarting retry....", pod.metadata.name, e))
            time.sleep(wait)
    raise Exception(str.format("Pod {0} has not been started", pod.metadata.name))


def create_deployment(path, yaml_file):
    v1 = get_kubernetes_dep_api_instance()
    with open(path + yaml_file) as f:
        dep = yaml.safe_load(f)
        resp = v1.create_namespaced_deployment(
            body=dep, namespace="default")
        print("Deployment created. status='%s'" % str(resp.status))


def exec_commands_on_pod(pod_name):
    api_instance = get_kubernetes_core_api_instance()
    resp = None
    try:
        resp = api_instance.read_namespaced_pod(name=pod_name,
                                                namespace='default')
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)
        raise e
    exec_command = [
        '/bin/sh',
        '-c',
        'ls']

    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  pod_name,
                  'default',
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    print("Response: " + resp)


def get_pod_status(pod_name):
    v1 = get_kubernetes_core_api_instance()
    return v1.read_namespaced_pod(name=pod_name,
                                  namespace='default').status.phase
