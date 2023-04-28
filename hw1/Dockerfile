FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y \
      libboost-all-dev \
      clang \
      cmake

ADD ./src /app/src

WORKDIR /app/src/lib/protobuf/build

RUN make install

WORKDIR /app/build

RUN cmake ../src && make

CMD ["./main"]
