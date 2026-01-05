#!/bin/bash
#script de nettoyage de l'app sur k8s

set -e

echo "Nettoyage"
echo ""

read -p "Êtes-vous sûr de vouloir supprimer l'application ? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Annulation"
    exit 1
fi

echo ""
echo "Suppression du namespace et des ressources..."

kubectl delete namespace nlp

echo ""
echo "Application supprimée"
echo ""


