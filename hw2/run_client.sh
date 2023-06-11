pip install -r requirements.txt
cd src
python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. mafia.proto
python3 client.py