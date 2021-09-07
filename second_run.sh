export CERT_MANAGER_VERSION=v1.3.0
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml
kubectl wait --for=condition=available --timeout=600s deployment/cert-manager-webhook -n cert-manager
TAG=v0.6.0
kubectl apply -f https://github.com/kubeflow/kfserving/releases/download/$TAG/kfserving.yaml
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80

