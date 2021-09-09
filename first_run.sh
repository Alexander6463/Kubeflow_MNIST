minikube start

export PIPELINE_VERSION=1.7.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
curl -sL https://istio.io/downloadIstioctl | sh -
export PATH=$PATH:$HOME/.istioctl/bin
kubectl apply -f https://github.com/knative/serving/releases/download/v0.24.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/v0.24.0/serving-core.yaml
istioctl install -f istio-minimal-operator.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/v0.24.0/net-istio.yaml
minikube tunnel


