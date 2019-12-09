# gRPC Error
fork from [](https://github.com/avinassh/grpc-errors/tree/master/python)

## Instructions

Install the dependencies:

    # pipenv install grpcio-tools --pypi-mirror https://mirrors.aliyun.com/pypi/simple
    $ pipenv install --dev

Generate protobuf files:

    $ python -m grpc_tools.protoc --proto_path=./ --python_out=./stub --grpc_python_out=./stub ./hello.proto

Run client and server:

    $ python server.py &
    $ python client.py