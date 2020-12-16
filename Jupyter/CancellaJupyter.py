from os import path
from kubernetes import client, config

DEPLOYMENT_NAME = "jupyter-deployment"
SERVICE_NAME = "jupyter-service"
INGRESS_NAME = "jupyter-ingress"

 
def delete_deployment(api_instance):
    api_response = api_instance.delete_namespaced_deployment(
        name=DEPLOYMENT_NAME,
        namespace="default",
        body=client.V1DeleteOptions(propagation_policy='Foreground',grace_period_seconds=5))
    print("Deployment deleted. status='%s'" % str(api_response.status))

def delete_service(api_instance):
    api_response = api_instance.delete_namespaced_service(
        name=SERVICE_NAME,
        namespace="default",
        body=client.V1DeleteOptions(propagation_policy='Foreground',grace_period_seconds=5))
    print("Service deleted. status='%s'" % str(api_response.status))

def cancella():

    config.load_kube_config()
    apps_v1_api = client.AppsV1Api()
    core_v1_api = client.CoreV1Api()
   
    delete_deployment(apps_v1_api)
    delete_service(core_v1_api)
   


if __name__ == '__main__':
    cancella()

