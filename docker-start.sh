#!/bin/sh

IMAGE=pylocating

CONTAINER=`docker ps | grep ${IMAGE} | head -n1 | rev | awk '{print $1}' | rev`

if [ -n "$CONTAINER" ]; then
  docker exec -i -t -u $IMAGE ${CONTAINER} /bin/bash
else
  docker run -i -t -u $IMAGE -v `pwd`:/home/pylocating/.virtualenvs/pylocating/src/pylocating:rw $IMAGE /bin/bash
fi

