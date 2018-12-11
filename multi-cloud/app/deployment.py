from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from app.gather_prices import read_prices_from_file
from app.config import GCP_PROJECT_ID, GCP_SECRET_KEY, GCP_CLIENT_ID, GCP_IMAGES_FILE, EC2_ACCESS_ID, EC2_SECRET_KEY, AWS_IMAGES_FILE


def deployment(NodeSize, os, name):
    # create driver

    if NodeSize.driver == get_driver(Provider.GCE):
        ComputeEngine = get_driver(Provider.GCE)
        gcp_driver = ComputeEngine(GCP_CLIENT_ID, GCP_SECRET_KEY, project=GCP_PROJECT_ID, datacenter="us-east1-b", auth_type="IA")
        images = read_prices_from_file(GCP_IMAGES_FILE)
        print(images[os])
        image = images[os]
        node = gcp_driver.create_node(name=name, size=NodeSize.name, image=image, location="us-east1-b")
        return node

    else:
        cls = get_driver(Provider.EC2)
        driver = cls(EC2_ACCESS_ID, EC2_SECRET_KEY, region="us-east-1")
        images = read_prices_from_file(AWS_IMAGES_FILE)
        image = images[os]
        node = driver.create_node(name=name, image=image, size=NodeSize)
        return node


def get_node(provider, id):
    if provider == 'Google':
        ComputeEngine = get_driver(Provider.GCE)
        gcp_driver = ComputeEngine(GCP_CLIENT_ID, GCP_SECRET_KEY, project=GCP_PROJECT_ID, datacenter="us-east1",
                                   auth_type="IA")
        node = gcp_driver.ex_get_volume(id, zone=all, use_cache=False)

    else:
        cls = get_driver(Provider.EC2)
        driver = cls(EC2_ACCESS_ID, EC2_SECRET_KEY, region="us-east-1")
        node = driver.list_nodes(ex_node_ids=[id], ex_filters=None)
        return node


def wait_for_node(provider, node):
    if provider == 'Google':
        ComputeEngine = get_driver(Provider.GCE)
        gcp_driver = ComputeEngine(GCP_CLIENT_ID, GCP_SECRET_KEY, project=GCP_PROJECT_ID, datacenter="us-east1",
                                   auth_type="IA")
        tuple = gcp_driver.wait_until_running(node)
    else:
        cls = get_driver(Provider.EC2)
        driver = cls(EC2_ACCESS_ID, EC2_SECRET_KEY, region="us-east-1")
        tuple = driver.wait_until_running(node)
        return tuple






