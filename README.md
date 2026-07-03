# 🚀 MLOps Project: Focused on End-to-End Operations

This repository contains an end-to-end Machine Learning Operations (MLOps) project demonstrating the complete lifecycle of a machine learning model. It covers everything from local experimentation and data versioning to containerized continuous deployment (CI/CD) and cluster monitoring on AWS.

## 🛠️ Tech Stack & Infrastructure
* **Cloud Provider:** Amazon Web Services (AWS) - EC2, EKS, ECR, S3, IAM, Elastic Load Balancing
* **Containerization & Orchestration:** Docker, Kubernetes (`kubectl`, `eksctl`)
* **CI/CD:** GitHub Actions
* **Experiment Tracking:** MLflow (hosted on DagsHub)
* **Data & Pipeline Versioning:** DVC (Data Version Control)
* **Model Serving:** Flask
* **Monitoring & Observability:** Prometheus, Grafana

---

## 🏗️ Project Architecture & Workflow

### 1. Local Setup & Project Structure
The project structure was bootstrapped using the Cookiecutter Data Science template.
```bash
# Create and activate environment
conda create -n atlas python=3.10
conda activate atlas

# Bootstrap structure
pip install cookiecutter
cookiecutter -c v1 [https://github.com/drivendata/cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science)

```

### 2. Experiment Tracking (MLflow via DagsHub)

All model experiments and metrics are tracked using MLflow integrated with DagsHub.

1. Connect the GitHub repo to [DagsHub](https://dagshub.com/dashboard).
2. Install tracking dependencies: `pip install dagshub mlflow`
3. Generate a DagsHub access token and store it as a GitHub Secret (`CAPSTONE_TEST`) for CI/CD authentication.

### 3. Data & Pipeline Versioning (DVC + AWS S3)

DVC is used to version large datasets and model artifacts, backed by an AWS S3 remote.

```bash
# Initialize DVC
dvc init

# Configure AWS IAM Credentials
aws configure 

# Add AWS S3 as the remote storage
pip install dvc[s3] awscli
dvc remote add -d myremote s3://<your-bucket-name>

# Execute pipeline and push artifacts to S3
dvc repro
dvc push

```

### 4. Containerization & Local Testing

The model is served via a Flask API, containerized using Docker.

```bash
# Generate requirements
pipreqs . --force

# Build the Docker image
docker build -t capstone-app:latest .

# Run locally (injecting DagsHub token for MLflow registry access)
docker run -p 8888:5000 -e CAPSTONE_TEST=<your_token> capstone-app:latest

```

### 5. CI/CD Pipeline (GitHub Actions -> AWS ECR)

Upon pushing to the `main` branch, a GitHub Actions workflow (`ci.yaml`) triggers, builds the Docker image, and pushes it to Amazon Elastic Container Registry (ECR).

**Required GitHub Secrets:**

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_REGION`
* `AWS_ACCOUNT_ID`
* `ECR_REPOSITORY` (e.g., `capstone-proj`)

*(Ensure the AWS IAM user has `AmazonEC2ContainerRegistryFullAccess`)*.

---

## ☸️ Kubernetes Deployment (AWS EKS)

The containerized application is deployed to an Amazon EKS cluster.

### Prerequisites

* Install `awscli` (Python-based or MSI installer).
* Install `kubectl` and `eksctl`.

```powershell
# Verify installations
aws --version
kubectl version --client
eksctl version

```

### Cluster Provisioning & Deployment

```bash
# 1. Create the EKS Cluster and NodeGroup
eksctl create cluster --name flask-app-cluster --region us-east-1 --nodegroup-name flask-app-nodes --node-type t3.small --nodes 1 --nodes-min 1 --nodes-max 1 --managed

# 2. Update kubeconfig to point to the new cluster
aws eks --region us-east-1 update-kubeconfig --name flask-app-cluster

# 3. Verify connectivity
kubectl get nodes

# 4. Deploy the application (Make sure inbound rules allow port 5000 on the node security group)
kubectl apply -f deployment.yaml

# 5. Retrieve the External IP of the LoadBalancer
kubectl get svc flask-app-service

```

You can now access the API via: `http://<external-ip>:5000`

---

## 📈 Monitoring & Observability

To monitor the health and performance of the EKS application, Prometheus and Grafana are configured on standalone EC2 instances (`t3.medium`).

### Prometheus Setup

1. Launch an Ubuntu EC2 instance. Allow inbound traffic on port `9090`.
2. Download and extract Prometheus.
3. Configure `prometheus.yml` to scrape the Flask app's LoadBalancer IP:
```yaml
scrape_configs:
  - job_name: "flask-app"
    static_configs:
      - targets: ["<external-ip>:5000"]

```


4. Start the Prometheus server.

### Grafana Setup

1. Launch an Ubuntu EC2 instance. Allow inbound traffic on port `3000`.
2. Install Grafana: `sudo apt install ./grafana_10.1.5_amd64.deb -y`
3. Start the service: `sudo systemctl start grafana-server`
4. Access Grafana at `http://<ec2-public-ip>:3000` (Default login: `admin`/`admin`).
5. Add the Prometheus server URL (`http://<prometheus-ec2-ip>:9090`) as a Data Source and build your dashboards.

---

## 🧹 AWS Resource Cleanup

To prevent ongoing cloud charges, all infrastructure must be torn down when not in use.

```bash
# 1. Delete Kubernetes resources
kubectl delete deployment flask-app
kubectl delete service flask-app-service
kubectl delete secret capstone-secret

# 2. Delete the EKS Cluster
eksctl delete cluster --name flask-app-cluster --region us-east-1

# 3. Verify EKS deletion (Checks CloudFormation stacks)
eksctl get cluster --region us-east-1

# 4. Additional Cleanup
# - Delete artifacts in S3 and Docker images in ECR via the AWS Console.
# - Terminate the EC2 instances running Prometheus and Grafana.

```

## 📝 Notes on AWS Limits

* **CloudFormation & EKS:** `eksctl` generates CloudFormation templates to provision the EKS control plane and node groups automatically.
* **Fleet Requests:** NodeGroups use Auto Scaling Groups (ASG) which count against your AWS account's Fleet Request quota. If deployment fails with "You’ve reached your quota for maximum Fleet Requests", check for orphaned ASGs or request a quota increase.

```

```
