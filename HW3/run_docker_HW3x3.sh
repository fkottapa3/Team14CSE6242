time docker container run -it --rm --network="host" \
  -v "$PWD/Q1:/root" \
  -e JUPYTER_RUNTIME_DIR=/tmp/jupyter_runtime \
  -p 6242:8888 \
  polodataclub/cse6242hw3-public:Q1
