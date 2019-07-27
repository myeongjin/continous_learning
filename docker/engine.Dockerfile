FROM tensorflow/tensorflow:1.14.0-py3

RUN python -m pip install --upgrade pip
RUN pip install grpcio grpcio-tools redis scikit-image

WORKDIR /root

COPY protobuf protobuf
ENV PYTHONPATH /root/protobuf
RUN python -m grpc_tools.protoc -I=protobuf engine.proto --python_out=protobuf --grpc_python_out=protobuf

COPY engine engine
