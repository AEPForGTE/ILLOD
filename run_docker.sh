#!/bin/bash

docker build -t illod .
echo "Running iterations for 10-fold validation ..."
docker run -v "$(pwd)"/MAIN/output_data_docker:/usr/ILLOD/MAIN/output_data illod
