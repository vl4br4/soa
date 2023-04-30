FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
      libboost-all-dev \
      clang \
      cmake \
      git

ADD ./src /app/src

WORKDIR /app/src/lib
RUN git clone https://github.com/msgpack/msgpack-c.git
RUN git clone https://github.com/nlohmann/json.git
RUN git clone https://github.com/Gregwar/mongoose-cpp.git
RUN git clone https://github.com/jbeder/yaml-cpp.git
RUN git clone https://github.com/confluentinc/avro-cpp-packaging.git

WORKDIR /app/src/lib/yaml-cpp/build
RUN rm -rf * && cmake .. && make && make install

WORKDIR /app/src/lib/json/build
RUN rm -rf * && cmake .. && make

WORKDIR /app/src/lib/avro-cpp-packaging/build
RUN rm -rf * && cmake .. && make

WORKDIR /app/src/lib/msgpack-c
RUN git checkout cpp_master && cmake . && cmake --build . --target install

WORKDIR /app/build

RUN cmake ../src && make

