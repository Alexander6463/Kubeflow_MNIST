import kfp
import kfp.components as components
import kfp.dsl as dsl

from components.download_component import download_dataset
from components.train_component import train_model
from components.evaluate_component import evaluate_model
from components.export_component import export_model

BASE_IMAGE = "drobnov1994/example:kubeflow_tensorflow_v1"
INPUT_BUCKET = "pipelines-tutorial-data"
NAMESPACE = "default"

kfserving = components.load_component_from_url(
    "https://raw.githubusercontent.com/kubeflow/pipelines/master/components/kubeflow/kfserving/component.yaml"
)


def train_and_serve(
    input_bucket: str,
    dataset_name: str,
    export_bucket: str,
    model_name: str,
    model_version: str,
):
    downloadOp = components.func_to_container_op(
        download_dataset, base_image=BASE_IMAGE
    )(input_bucket, dataset_name)
    downloadOp.execution_options.caching_strategy.max_cache_staleness = "P0D"
    trainOp = components.func_to_container_op(train_model, base_image=BASE_IMAGE)(
        downloadOp.output
    )
    trainOp.execution_options.caching_strategy.max_cache_staleness = "P0D"
    evaluateOp = components.func_to_container_op(evaluate_model, base_image=BASE_IMAGE)(
        downloadOp.output, trainOp.output
    )
    evaluateOp.execution_options.caching_strategy.max_cache_staleness = "P0D"
    exportOp = components.func_to_container_op(export_model, base_image=BASE_IMAGE)(
        trainOp.output, evaluateOp.output, export_bucket, model_name, model_version
    )
    exportOp.execution_options.caching_strategy.max_cache_staleness = "P0D"
    kfservingOp = kfserving(
        action="apply",
        model_uri=f"s3://{export_bucket}/{model_name}",
        model_name="mnist",
        namespace=NAMESPACE,
        framework="tensorflow",
        watch_timeout="300",
    )
    kfservingOp.after(exportOp)
    kfservingOp.execution_options.caching_strategy.max_cache_staleness = "P0D"


def op_transformer(op):
    op.add_pod_annotation(name="sidecar.istio.io/inject", value="false")
    return op


@dsl.pipeline(
    name="End-to-End MNIST Pipeline",
    description="A sample pipeline to demonstrate "
    "multi-step model training,"
    "evaluation, export, and serving",
)
def mnist_pipeline(
    input_bucket: str = "pipelines-tutorial-data",
    dataset_name: str = "datasets.tar.gz",
    export_bucket: str = "models",
    model_name: str = "mnist",
    model_version: str = "1",
):
    train_and_serve(
        input_bucket=input_bucket,
        dataset_name=dataset_name,
        export_bucket=export_bucket,
        model_name=model_name,
        model_version=model_version,
    )
    dsl.get_pipeline_conf().add_op_transformer(op_transformer)


arguments = {
    "input_bucket": INPUT_BUCKET,
    "dataset_name": "datasets.tar.gz",
    "export_bucket": "models",
    "model_name": "mnist",
    "model_version": "1",
}

client = kfp.Client(host="http://127.0.0.1:8080")
client.create_run_from_pipeline_func(train_and_serve, arguments=arguments)
