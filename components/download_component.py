from kfp.components import OutputPath


def download_dataset(data_dir: OutputPath(str), input_bucket: str, dataset_name: str):
    """Download the MNIST data set to the Kubeflow Pipelines
    volume to share it among all steps"""
    import tarfile
    import os
    from minio import Minio

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    client = Minio("minio-service:9000", "minio", "minio123", secure=False)
    client.fget_object(input_bucket, dataset_name, dataset_name)
    tar = tarfile.open(name="datasets.tar.gz", mode="r|gz")
    tar.extractall(path=data_dir)
