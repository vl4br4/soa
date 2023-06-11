FROM python

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
WORKDIR /app/src
RUN python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. mafia.proto

ENTRYPOINT [ "python3", "server.py" ]