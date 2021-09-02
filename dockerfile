from python:3.8

RUN pip install tensorflow
RUN pip install tensorflow_datasets
Run pip install minio

EXPOSE 8000
CMD ["/bin/bash"]