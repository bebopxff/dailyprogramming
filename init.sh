#!/bin/env bash

set -x

PROJ=$(date +'%Y/%m/%d')
if [ -d "$RPOJ" ]
then
  echo "Directory $RPOJ exists."
else
  echo "Directory $RPOJ DOES NOT exists."
  mkdir -p $PROJ
fi

cd $PROJ
touch $1