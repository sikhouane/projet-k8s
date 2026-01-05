# Projet Kubernetes


- Prérequis

**kubectl**
**Docker**
**gcloud CLI**


1. Authentification GCP
gcloud auth login
gcloud auth application-default login
gcloud config set project projet-k8s-483316

2. Déploiement de Terraform
Initialisation
cd terraform/gke
terraform init
terraform plan
terraform apply

Récupération du kubeconfig
gcloud container clusters get-credentials projet-k8s-gke-cluster \
  --zone europe-west3-a \
  --project projet-k8s-483316

Vérification
kubectl get nodes

3. Artifact Registry (Docker images)
Création du repo
gcloud services enable artifactregistry.googleapis.com

gcloud artifacts repositories create nlp-repo \
  --repository-format=docker \
  --location=europe-west3 \
  --description="Images projet k8s"

Auth Docker
gcloud auth configure-docker europe-west3-docker.pkg.dev

4. Build & Push des images Docker
Backend
docker build \
  -t europe-west3-docker.pkg.dev/projet-k8s-483316/nlp-repo/nlp-back:1.0 \
  -f NLP_Project/Dockerfile \
  NLP_Project

docker push europe-west3-docker.pkg.dev/projet-k8s-483316/nlp-repo/nlp-back:1.0

Frontend
docker build \
  -t europe-west3-docker.pkg.dev/projet-k8s-483316/nlp-repo/nlp-front:1.0 \
  -f frontend/Dockerfile \
  frontend

docker push europe-west3-docker.pkg.dev/projet-k8s-483316/nlp-repo/nlp-front:1.0

5. Droits IAM pour GKE (obligatoire)
PROJECT_ID=projet-k8s-483316
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/artifactregistry.reader"

6. Déploiement Kubernetes
kubectl apply -f k8s/

Vérification
kubectl get pods -n nlp
kubectl get svc -n nlp

7. Installation de l’Ingress NGINX
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.9.5/deploy/static/provider/cloud/deploy.yaml

Vérification
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx

8. Vérification de l’Ingress applicatif
kubectl get ingress -n nlp

Récupérer l’IP publique :

ADDRESS: 35.xxx.xxx.xxx

9. Tests fonctionnels
Variable d’environnement
export INGRESS_IP=35.xxx.xxx.xxx

Health check
curl -i http://$INGRESS_IP/api/health -H "Host: nlp.example.com"

Requête NLP
curl -i http://$INGRESS_IP/api/ask -H "Host: nlp.example.com" \
  -H "Content-Type: application/json" \
  --data-raw "{\"question\":\"Quelle est la meteo a Paris demain a 15h ?\"}"


Réponse attendue :

{
  "question": "...",
  "answer": "Météo à Paris le 2026-01-05 15:00 : pluvieux, 10.6°C..."
}

10. Test interne Kubernetes (DNS & Services)
kubectl run curltest -n nlp \
  --image=curlimages/curl:8.5.0 \
  -it --rm -- sh


Dans le pod :

curl http://nlp-back-svc/health
curl -X POST http://nlp-back-svc/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"test"}'
exit

11. Nettoyage
kubectl delete -f k8s/
terraform destroy