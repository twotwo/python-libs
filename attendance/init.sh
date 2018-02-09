#!/bin/sh
[ -d env ] && \
  echo "run " source env/bin/activate && exit || \
  echo "init env..."
  virtualenv env
  env/bin/pip install xlrd xlwt jinja2