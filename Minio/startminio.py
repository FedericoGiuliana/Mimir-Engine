from kubernetes import client, config
import time
import os 

MINIO_ACCESS_KEY=os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.environ.get("MINIO_SECRET_KEY")

def create_deployment(apps_v1_api,env_vars=None):

    if env_vars is None:
        env_vars = {"MINIO_ACCESS_KEY":MINIO_ACCESS_KEY,"MINIO_SECRET_KEY":MINIO_SECRET_KEY}
    env_list = []
    for env_name, env_value in env_vars.items():
        env_list.append( client.V1EnvVar(name=env_name, value=env_value) )

    volume = client.V1Volume(
        name="data"
    )

    container = client.V1Container(
        name="minio",
        image="minio/minio",
        args=["server","/data"],
        volume_mounts=[client.V1VolumeMount(name="data",mount_path="/data")],
        env=env_list,
        image_pull_policy="Always",
        ports=[client.V1ContainerPort(container_port=9000)],
    )
    
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "minio"}),
        spec=client.V1PodSpec(volumes=[volume],containers=[container]))
    
    spec = client.V1DeploymentSpec(
        selector=client.V1LabelSelector(match_labels={"app":"minio"}),
        replicas=1,
        template=template)
    
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="minio-deployment",labels={"app":"minio"}),
        spec=spec)
    
    
    apps_v1_api.create_namespaced_deployment(
        namespace="default", body=deployment
    )


def create_service():
    core_v1_api = client.CoreV1Api()
    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            labels={"app":"minio"},
            name="minio-service"
        ),
        spec=client.V1ServiceSpec(
            type="NodePort",
            selector={"app": "minio"},
            ports=[client.V1ServicePort(
                protocol="TCP",
                port=9000,
                target_port=9000,
                node_port=31000
            )]
        )
    )

    core_v1_api.create_namespaced_service(namespace="default", body=body)

def create_ingress(networking_v1_beta1_api):

    body = client.NetworkingV1beta1Ingress(
        api_version="networking.k8s.io/v1beta1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(name="minio-ingress", labels={"app":"minio"}, annotations={
            "nginx.ingress.kubernetes.io/rewrite-target": "/"
        }),
        spec=client.NetworkingV1beta1IngressSpec(
            rules=[client.NetworkingV1beta1IngressRule(
                host="minio.kubernetes.local",
                http=client.NetworkingV1beta1HTTPIngressRuleValue(
                    paths=[client.NetworkingV1beta1HTTPIngressPath(
                        path="/",
                        backend=client.NetworkingV1beta1IngressBackend(
                            service_port=9000,
                            service_name="minio-service")

                    )]
                )
            )
            ]
        )
    )
    networking_v1_beta1_api.create_namespaced_ingress(
    namespace="default",
    body=body
    )
def crea():
   
    config.load_kube_config()
    apps_v1_api = client.AppsV1Api()
    networking_v1_beta1_api = client.NetworkingV1beta1Api()

    
    create_deployment(apps_v1_api)
    create_service()
    create_ingress(networking_v1_beta1_api)


if __name__ == "__main__":
    crea()
