# conda-random-solver

A test of the conda plugin system. This plugin ties into the solver
plugin endpoint. It picks 10 random packages within the channels you
have chosen.

```shell
$ docker run -it --rm --platform=linux/amd64 \
  -v $PWD/:/opt/conda-random-solver-src \
  ghcr.io/conda/conda-ci:main-linux-python3.9 bash

$ pip install -e .
```
