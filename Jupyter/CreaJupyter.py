from kubernetes import client, config
import time

def create_deployment(apps_v1_api):
    container = client.V1Container(
        name="jupyter",
        image="jupyter/minimal-notebook",
        command=["jupyter", "notebook", "--NotebookApp.token=''"],
        image_pull_policy="Always",
        ports=[client.V1ContainerPort(container_port=8888)],
    )
    
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "jupyter-notebook"}),
        spec=client.V1PodSpec(containers=[container]))
    
    spec = client.V1DeploymentSpec(
        selector=client.V1LabelSelector(match_labels={"app":"jupyter-notebook"}),
        replicas=1,
        template=template)
    
    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name="jupyter-deployment",labels={"app":"jupyter-notebook"}),
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
            labels={"app":"jupyter-notebook"},
            name="jupyter-service"
        ),
        spec=client.V1ServiceSpec(
            type="NodePort",
            selector={"app": "jupyter-notebook"},
            ports=[client.V1ServicePort(
                protocol="TCP",
                port=8888,
                target_port=8888
            )]
        )
    )

    core_v1_api.create_namespaced_service(namespace="default", body=body)


def create_ingress(networking_v1_beta1_api):
    body = client.NetworkingV1beta1Ingress(
        api_version="networking.k8s.io/v1beta1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(name="jupyter-ingress", labels={"app":"jupyter-notebook"}, annotations={
            "nginx.ingress.kubernetes.io/rewrite-target": "/"
        }),
        spec=client.NetworkingV1beta1IngressSpec(
            rules=[client.NetworkingV1beta1IngressRule(
                host="pippo.notebooks.kubernetes.local",
                http=client.NetworkingV1beta1HTTPIngressRuleValue(
                    paths=[client.NetworkingV1beta1HTTPIngressPath(
                        path="/",
                        backend=client.NetworkingV1beta1IngressBackend(
                            service_port=8888,
                            service_name="jupyter-service")

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