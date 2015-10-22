#!/bin/sh

docker run -i -t --rm -v `pwd`:/pylocating:rw python:2-slim /bin/bash
