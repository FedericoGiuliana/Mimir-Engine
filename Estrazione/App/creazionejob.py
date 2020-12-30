#!/usr/bin/env/python
from os import path
import os
import yaml
import time
from kubernetes import client, config

ENDPOINT=os.environ.get("ENDPOINT")
MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")
BUCKET=os.environ.get("BUCKET")

def make_job_object(filename,filepath,id_training):
    env_vars=None
    if env_vars is None:
    	env_vars ={"ENDPOINT":ENDPOINT ,"MINIO_ACCESS_KEY":MINIO_ACCESS_KEY , "MINIO_SECRET_KEY" : MINIO_SECRET_KEY , "BUCKET": BUCKET , "FILENAME":str(filename), "FILEPATH": str(filepath),"ID_TRAINING":str(id_training)}
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append( client.V1EnvVar(name=env_name, value=env_value) )


    container = client.V1Container(
        name="estratto",
        image="ziofededocker/dummy:latest",
        command=["python","/app/estrazione.py"],
        env=env_list,
        image_pull_policy="IfNotPresent")


    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "estratto"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))

    spec = client.V1JobSpec(
        template=template,
        backoff_limit=0)

    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name="estrazione-job"),
        spec=spec)

    return job


def create_job(api_instance, job):
    api_response = api_instance.create_namespaced_job(
        body=job,
        namespace="default")
    print("Job created. status='%s'" % str(api_response.status))


def update_job(api_instance, job):

    job.spec.template.spec.containers[0].image = "ziofededocker/dummy:latest"
    api_response = api_instance.patch_namespaced_job(
        name="estrazione-job",
        namespace="default",
        body=job)
    print("Job updated. status='%s'" % str(api_response.status))
    
    
def delete_job(api_instance):
    api_response = api_instance.delete_namespaced_job(
        name="estrazione-job",
        namespace="default",
        body=client.V1DeleteOptions(propagation_policy='Foreground',grace_period_seconds=5))
    print("Job deleted. status='%s'" % str(api_response.status))


def creajob(filename,filepath,id_training):

    config.load_kube_config()
    batch_v1 = client.BatchV1Api()

    job = make_job_object(filename,filepath,id_training)

    create_job(batch_v1, job)

    update_job(batch_v1, job)
    
    time.sleep(5)
    
    delete_job(batch_v1)


if __name__ == '__main__':
    creajob()
