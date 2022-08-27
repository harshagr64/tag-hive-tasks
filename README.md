# Taghive DevOps Homework Assignment

## Process/Solution

For simplicity of this assignment, I have used a single node k8s cluster i.e. minikube. 

app_b requires sqlite db connectivity for its working. for simplicity, I have manually created a DB(database.db) that has sample data from schema.sql file and it will be diretly passed inside the Dockerfile so, whenever a container runs from the resulting image, it will be able to connect to the database easily. I know it is not an optimal solution but as this app is very basic, so I used this approach.

In real world application, there will always be a secured instance/container for database will be running which is not accessible publicly. Only authenticated & authorized application will have access.

### changes in the pre-defined applications

- I have created wsgi.py file in both the applications so that gunicorn server will be used to run application in production.
- To use gunicorn in flask application, I have added gunicorn latetst version in requirements.txt file for both the application.

### Dockerfiles

I have created seperate Dockerfiles for both the apps with following consideration:
 - Used latest python 3.10.6 version with minimum base image.
 - app will always run as non-root user to prevent any privilege escalations. User I have created is python because When creating a Docker container, by default, it will run it as root. Although this is convenient for development, but not recommended in production images. Suppose, for whatever reason, an attacker has access to a terminal or can execute code. In that case, it has significant privileges over that running container, as well as potentially accessing host filesystems via filesystem bind mounts with inappropriately high access rights.
 - I have created a virtual environment for application inside docker container because it is not recommended to run pip that comes pre-installed with python base images as it will run as a root user.
 - gunicorn server is used to serve these applications which is recommended for production use.
 - I have created .dockerignore file for both the apps because I want to make sure that the final Image is of smaller size. so, I have excluded files that are not required by container to run application.
 - I have applied the possible owasp guidelines for creating docker images.
 - ##### Bonus Point:
    - As these apps are very basic, so there is no need to use multi-stage build(build & deploy stage) in the Dockerfile because it will increase build time for docker image.

### k8s-deployment

I have created 2 seperate deployment files for both the apps with the following consideration:
 - I have created a ClusterIP service for app_b as it is not accessed by end user and internally app_a will be calling app_b.
 - I have created a NodePort service for app_a as it will be accessed by end user.
 - As it is a basic app, so I have created 1 replicas for both the application.
 - I have defined resource quota for the both the apps. so, that they do not consume resouces more than specified in their resource limits. If I do not specify resource quota, then container running inside pod can take whatever amount of resource available on the host.
 - k8s by default pull docker images from docker hub(docker.io official registry). In this task, I will be building images from Dockerfile. I also need to to publish it to docker hub so that k8s can pull these images, But to do so, firstly, I need to login to docker hub & push docker images on it. Now, to achieve this using Taskfile.yml, I have to specify my docker hub credentials in this file, which is not a proper aprroach.  
 - to solve the above problem, I have added imagePullPolicy to Never in container specs.



### Taskfile.yml

I have included 4 tasks in Taskfile.yml:
 - run-app (main-task)
 - build-task (to build docker images from Dockerfile)
 - scan-images (to scan both the image using snyk)
 - deploy-task (to deploy both the apps in k8s cluster)

Firstly, Taskfile will be scaning the images from their Dockerfile. Secondly, as I want k8s to pull docker images from the machine so, I have to run it from docker-daemon of minikube so that k8s will be able to pull images from machine. (Images that are not build from docker daemon of minikube, k8s will not be able to run containers using them) and hence, I have used "eval" command. Lastly, I will deploy containers using k8s deployment file.

I will be scanning the image using Dockerfile first, because after applying "eval" command, every docker command will run from docker daemon of minikube and this docker daemon is not able to scan images using snyk without sudo and hence task will fail to execute.

## Running the assignment

### Prerequisite:

- Docker installed & running on system & snyk comes preinstalled with docker
- Minikube installed & running on system
- task installed on system

To get minikube node ip
```bash
minikube ip
```

Running the apps locally:
```bash
task run-app
```

Making a request:

```bash
curl http://<minikube_ip>:32000/hello

curl -X POST -H 'Authorization: mytoken' http://<minikube_ip>:32000/jobs
```

Simulating a lot of requests

```bash
ab -m POST -H "Authorization: mytoken" -n 500 -c 4 http://<minikube_ip>:32000/jobs
```
