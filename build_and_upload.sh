#!/bin/bash



docker build -t roboharbor/validate-robot .

docker push roboharbor/validate-robot


docker build --no-cache -t roboharbor/robo-pier-python .

docker push roboharbor/robo-pier-python