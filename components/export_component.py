from kfp.components import InputPath


def export_model(
    model_dir: InputPath(str),
    metrics: InputPath(str),
    export_bucket: str,
    model_name: str,
    model_version: str,
):
    import os
    from minio import Minio

    client = Minio("minio-service:9000", "minio", "minio123", secure=False)

    # Create export bucket if it does not yet exist
    if not client.bucket_exists(export_bucket):
        client.make_bucket(export_bucket)

    # Save model files to minio
    for root, dirs, files in os.walk(model_dir):
        for filename in files:
            local_path = os.path.join(root, filename)
            minio_path = os.path.relpath(local_path, model_dir)
            client.fput_object(
                export_bucket,
                os.path.join(model_name, model_version, minio_path),
                local_path,
            )

    response = client.list_objects(export_bucket, recursive=True)
    print(f"All objects in {export_bucket}:")
    for file in response:
        print(file.object_name)
