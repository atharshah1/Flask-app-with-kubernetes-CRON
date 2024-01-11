
# Flask-app-with-kubernetes-CRON

A case study to deploy webapp, flask backend, database and a python scrapper and alert.





## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

setup your minikube

```bash
  minikube start
```

Create secrets for the following required env variables:

DB_USERNAME 

EMAIL_PASS

DB_PASSWORD

```bash
  kubectl create secret generic test-db-secret --from-literal=username=# --from-literal=password=# --from-literal=email=#
```
(note - replace # with your values and the 'test-db-secret' is the name of the secret if you change it you need to change it on the yaml files [cron.yaml,dep_service.yaml,psql.yaml])

Deploy your database 

```bash
kubectl apply -f psql.yaml
```
Edit the url in html>script tag> fetch:
just edit the ip from the minikube ip don't change the port.

to get minikube ip:

```bash
minikiube ip
```

Build docker images d1, d2, d3 and push it to the repository and edit the values from the image field in the yaml files.

now deploy 'cron.yaml' and 'dep_service.yaml' using kubectl apply.

expose both the services d1-service and d2-service in minikube by the commnd

```bash
minikube service #nameoftheservice
```

