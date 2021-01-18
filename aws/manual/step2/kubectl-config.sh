#!/bin/bash


aws eks update-kubeconfig \
  --region us-west-2 \
  --name my-cluster

#aws sts get-caller-identity

#aws eks update-kubeconfig \
#    --region us-west-2 \
#    --name my-cluster \
#    --role-arn arn:aws:iam::867975079432:role/myAmazonEKSClusterRole


kubectl get svc