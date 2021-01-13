FROM ubuntu:18.04

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y python3 python3-dev python3-pip

RUN apt-get -y install gcc

RUN mkdir hyacc

RUN mkdir out
COPY hyacc/hyacc_unix_src_04-08-09.tar.gz ./hyacc/

RUN cd /hyacc && tar xvf hyacc_unix_src_04-08-09.tar.gz && make release

COPY grammars/ ./grammars/

COPY *.py ./

ENTRYPOINT python3 main.py -f $GRAMMAR_PATH  -l LR0 -g full-return -c $TEST_CASE_TYPE -o result
#ENTRYPOINT ls hyacc
