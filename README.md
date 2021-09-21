This is demo how to train MNIST model in Kubeflow Pipelines and deploy model with KFServing

## _Installing kubectl_
1. `snap install kubectl --classic`
2. `kubectl version --client`

## _Installing minikube_
1. `curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64`
2. `sudo install minikube-linux-amd64 /usr/local/bin/minikube`

## _Installing KFserving and Kubeflow Pipelines_
1. `minikube start --cpus 4 --memory 12288`
2. Install Kubeflow Pipelines
```
export PIPELINE_VERSION=1.7.0
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"`
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io`
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
```
3. Install Istio and KNative
```
curl -sL https://istio.io/downloadIstioctl | sh -
export PATH=$PATH:$HOME/.istioctl/bin
kubectl apply -f https://github.com/knative/serving/releases/download/v0.24.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/v0.24.0/serving-core.yaml
istioctl install -f istio-minimal-operator.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/v0.24.0/net-istio.yaml
```
4. Run `minikube tunnel` in command line
5. Install KFserving
```
export CERT_MANAGER_VERSION=v1.3.0
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/${CERT_MANAGER_VERSION}/cert-manager.yaml
kubectl wait --for=condition=available --timeout=600s deployment/cert-manager-webhook -n cert-manager
TAG=v0.6.0
kubectl apply -f https://github.com/kubeflow/kfserving/releases/download/$TAG/kfserving.yaml
```
6. Wait when all pods in the cluster will be in `Running` status (use command `kubectl get pods -A` to check it)
7. Then you need to deploy minio-secret.yaml, by using command `kubectl apply -f minio-secret.yaml`
8. And run the next command for setting up service account parameters: `kubectl create clusterrolebinding pipeline-runner-extend --clusterrole cluster-admin --serviceaccount=kubeflow:pipeline-runner`

## _Port forwarding for minio, kubeflow pipelines and Models UI_
1. For Kubeflow Pipelines use command:
- `kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80`
2. For Minio use command:
`kubectl port-forward svc/minio-service -n kubeflow 9000:9000`
3. For Models UI you need to set the ENV vars in the app's Deployment:
- Run `kubectl edit -n kfserving-system deployments.apps kfserving-models-web-app`
- Add next env variables: APP_PREFIX: "/", APP_DISABLE_AUTH: "True", APP_SECURE_COOKIES: "False"
- Run `kubectl port-forward -n kfserving-system svc/kfserving-models-web-app 5000:80`

## _Download datasets to Minio service_
1. Use the mc alias set command to add an Amazon S3-compatible service to the mc: 
- `mc alias set minio http://localhost:9000/ minio minio123`
2. Create bucket: `mc mb minio/pipelines-data-tutorial`
3. Copy dataset into bucket: `mc cp datasets.tar.gz minio/pipelines-data-tutorial`

After that you can run MNIST pipeline in Kubeflow Pipelines by command:
- `python3 pipeline_dev.py`

And finally, you need to check that your model is up in the cluster:
- `kubectl get inferenceservice mnist -n default`

Example of predict with MNIST model you can see in predict.sh, but before run it you need to create input.json file by using image_transform.py


