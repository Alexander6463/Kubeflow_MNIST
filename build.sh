#!/bin/bash -e
export image_name=kubeflow_mnist
export image_tag=kubeflow_tensorflow_v1
export full_image_name=${image_name}:${image_tag}

cd "$(dirname "$0")"
docker login
docker build -t "${image_tag}" .
docker tag $image_tag drobnov1994/example:$image_tag
docker push drobnov1994/example:$image_tag