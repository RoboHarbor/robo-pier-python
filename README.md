# robo-pier-ptyhon
## Docker Container for Running Python Scripts with RoboHarbor

This is a docker container that will be used from RoboHarbor when selecting the Python environment. 

The container is started with some paramaters, for example the repository to clone and the script to run.

The container will clone the repository, install the requirements and run the script.

The container will also send the log output back to RoboHarbor.

It also automatically sends status updates to RoboHarbor.

The container is started with the following command:

```bash

docker run -e ROBO_HARBOR=http://roboharbor:5000 -e ROBO_ID=my-robot -e ROBO_SECRET=secret

```

## Parameter Details

|        Name        |     Default Value      |                                          Description                                          |
|:------------------:|:----------------------:|:---------------------------------------------------------------------------------------------:|
|    ROBO_HARBOR     | http://roboharbor:5000 |                              The URL of the RoboHarbor instance                               |
|      ROBO_ID       |        my-robot        |                                      The ID of the robot                                      |
|    ROBO_SECRET     |         secret         |                                    The secret of the robot                                    |
| ONLY_TEST_CHECKOUT |         false          | This parameter is used only to test if the checkout works. After checkout the pod is deleted. |


