# Core Engine 

## Setup
Using Helm3 to install 

Pull chart from repo
```
helm pull asia-southeast1-docker.pkg.dev/airasia-goquo-dev/ota/charts/core-engine --version=1.0.0 -d /tmp
```

Install chart
```
helm install core-engine /tmp/core-engine-1.0.0.tgz --namespace=dev/staging/production --create-namespace 
```

