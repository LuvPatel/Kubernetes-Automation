
# Google Cloud Platform (GCP) with Terraform, Kubernetes and CI/CD Automation


This project illustrates the understanding of Google Cloud Platform (GCP) using Terraform to build a Kubernetes cluster from the ground up. It guides through the GCP Cloud Shell, where we can create and manage the GKE cluster. The project also demonstrates a CI/CD pipeline that automatically deploys a new image to the GKE cluster whenever code changes are made. All tasks are performed within the Cloud Shell, with the code sourced directly from the Github Repository. This project offers a thorough introduction to GKE, Terraform, and CI/CD pipelines.

### Key Highlights
* **Deep Dive into Kubernetes:** The project offers an in-depth exploration of Kubernetes, focusing on the creation of pods, persistent volumes, and services through Kubernetes deployment files
* **Provisioning Resources on Google Cloud Platform (GCP) with Terraform:** This project demonstrates the setup and management of GCP resources using Terraform, a robust Infrastructure as Code (IaC) tool.
* **Artifact Registry:** The project utilises the Artifact Registry, used for storing container images and other artifacts.
* **Utilizing Github for Version Control:** The project leverages Github for code storage and version control. Automatic build and deployment processes are triggered with each code push.

### Project Walkthrough

***Prerequisites*** :
* Basic working knowledge of Kubernetes, GKE and Terraform

To get started with this project, kindly follow the video provided below.


https://github.com/user-attachments/assets/d5180ce0-07dc-4656-936d-23cd1a3c12ec


I have used Terraform to provision the following key components :
* **Google Container Cluster**
* **Google Container Node Pool**
*  **Google Compute Disk**

Lets go over the Terraform Script now:

```
resource "google_container_cluster" "k8s-cluster" {
      name     = "k8s-cluster"
      location = var.location
    
      initial_node_count = var.node_count
    
      node_config {
        machine_type = "e2-small"
        disk_size_gb = 20
        disk_type    = "pd-standard"
      } 
    }

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.20.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}
```

Using the above script, a Google Kubernetes Engine (GKE) cluster, a node pool, and a compute disk have been set up, with careful configuration of each resource to ensure optimal performance.


### Build and Deploy

Once the above resources are provisioned through terraform on Google Cloud Platform [GCP], we need to build and deploy our application onto Google Kubernetes Engine (GKE). For this, I have used the following GCP resources:   

* **Github** : This is the place where the code is stored and the code versioning takes place.
* **Code Build** : The tool that is used to build and beploy the images.
* **Artifact Registry** : A storage space for our containerized images.
* **Trigger** : It executes the build and deployment process whenever there's a code push to our github repository.


So, whenever there is a new commit in our github repository, it will execute the GCP trigger. This builds and store the docker image and stores the image in the Artifact Registry. Later, the image is then deployed to the GKE cluster built earlier.

Next, lets look at the cloudbuild.yaml:

### CloudBuild.yml
This file specifies the build and steps to deploy. The process includes detailed steps for building the container image, pushing it to the GCP artifact registry , then finally  deploying the kubernetes workload to the GKE cluster.

```
teps:
# Step 1: Docker Build
# - Create a docker image from Github Repository
# - Create 2 tags for the same docker image. Commit ID and Latest.
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', '-t', '${_IMAGE_NAME}:$SHORT_SHA', '-t', '${_IMAGE_NAME}:latest', '.']

# Step 2: Docker Push
# - Push image to GCP Artifact Registry
- name: 'gcr.io/cloud-builders/docker'
  args: ['push', '--all-tags', '${_IMAGE_NAME}']

# Step 3: Deploy the kubernetes workload to GKE cluster. (i.e. deployment.yaml, service.yaml and pvc.yaml)
- name: "gcr.io/cloud-builders/gke-deploy"
  args:
  - run
  - --filename=./k8s
  - --image=${_IMAGE_NAME}:$SHORT_SHA
  - --location=${_CLUSTER_LOCATION}
  - --cluster=${_CLUSTER_NAME}

options:
  logging: CLOUD_LOGGING_ONLY
```

### Deployment.yaml

It creates Kubernetes objects on GKE and includes the configuration for a PersistentVolume, a PersistentVolumeClaim, a Deployment, and a Service.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1-deployment
  labels:
    app: app1
spec:
  replicas: 1
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
      - name: app1-container
        image: us-docker.pkg.dev/PROJECT_ID/PROJECT_NAME/app1:latest
        volumeMounts:
        - mountPath: /PV_dir
          name: standard-volume
      volumes:
      - name: standard-volume
        persistentVolumeClaim:
          claimName: standard-rwo-pvc
```

### PVC.yml

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: standard-rwo-pvc
spec:
  storageClassName: standard-rwo
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

### Service.yml

```
apiVersion: v1
kind: Service
metadata:
  name: app1-service
  labels:
    app: app1
spec:
  type: LoadBalancer
  selector:
    app: app1
  ports:
  - port: 80
    targetPort: 6000
```

Thus, this is all we need to deploy our application to the GKE cluster, by leveraging the power of GCP.
