from python:3.8

RUN pip install tensorflow, tensorflow_datasets, minio

EXPOSE 8000
CMD ["/bin/bash"]