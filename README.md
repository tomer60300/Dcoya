# Project Documentation: Dcoya Application

## Overview

This project is a web-based application that displays the current date and time, along with the machine name. 
It is built with HTML, JavaScript, 
and powered by a Nginx and deployable on a Kubernetes cluster.

## Project Structure

```
Dcoya/
│
├── certs/
│ ├── dcoya-app.crt
│ └── dcoya-app.key
├── docker/
│ └── dockerfile
├── config/
│ └── .env
├── nginx/
│ └── nginx.conf
├── src/
│ ├── index.html
│ └── script.js
├── k8s/
│ └── deployment.yaml
├── scripts/
│ ├── config.py
│ ├── requirements.txt
│ └── status_check.py
└── README.md
```


### Key Components

- **certs/**: Contains SSL certificates for HTTPS.
- **docker/dockerfile**: Docker configuration file for building the application image.
- **config/.env**: Environment file storing configuration variables.
- **nginx/nginx.conf**: Nginx configuration file.
- **src/**: Contains the front-end files (`index.html` and `script.js`).
- **k8s/deployment.yaml**: Kubernetes deployment and service configuration.
- **scripts/**: Contains Python scripts for automated testing and configuration.
- **README.md**: Documentation for the project.

## Setup and Deployment

### Prerequisites

- Docker
- Kubernetes (for K8s deployment)
- Python 3 (for running the test script)

### Building the Docker Image

Navigate to the root of the project and run:

```bash
docker build -f docker/dockerfile -t dcoya-app .
```
### Running the Docker Container
```bash
docker run --name dcoya-app -p 443:443 --env-file ./config/.env -d dcoya-app
```
### Deploying to Kubernetes
Apply the Kubernetes deployment:
```bash
kubectl apply -f k8s/deployment.yaml
```

### Accessing the Application

The application can be accessed at https://localhost or the IP of your Kubernetes cluster.

### Tests
The scripts in the scripts/ directory perform automated tests to ensure the application is running correctly.
#### Running the Test Scripts
Install dependencies:
```bash
pip install -r scripts/requirements.txt
```
Run the test script:
```bash
python scripts/status_check.py
```

### Certificates
To create self sign certificates run the following commands:

First create a openssl.cnf with the following content
```text
[req]
default_bits       = 2048
prompt             = no
default_md         = sha256
distinguished_name = dn
req_extensions     = req_ext

[ dn ]
C            = Country
ST           = District
L            = City
O            = "Your Organization"
OU           = "Your Organization"
emailAddress = "Your Email"
CN           = <host name>

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1   = <host name DNS name>
IP.1    = <App exposed IP>
```
Then start creating the public and private keys for your app 
```bash
 openssl x509 -req -days 30 -in dcoya-app.csr -signkey dcoya-app.key -out dcoya-app.crt -extensions req_ext -extfile openssl.cnf
```

```bash
openssl req -new -nodes -out dcoya-app.csr -config openssl.cnf -keyout dcoya-app.key
```
Now move the .crt and .key files into your project certs/ directory 
