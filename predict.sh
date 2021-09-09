set -o errexit
model="mnist"
url="http://${model}.default.svc.cluster.local/v1/models/${model}:predict"

curl --fail -L "${url}" -d@input.json -o output.json
