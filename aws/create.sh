# prerequisites: https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

eksctl create cluster \
--name my-cluster \
--region us-west-2 \
--with-oidc \
--ssh-access \
--ssh-public-key udacity-key \
--managed


# View your cluster nodes.
kubectl get nodes -o wide

# View the workloads running on your cluster.
kubectl get pods --all-namespaces -o wide


kubectl get all -n default


kubectl -n default describe service kubernetes


kubectl -n default describe pod inventory


# Execute a shell on one of the pods by replacing the <value> below with a value returned for one of your pods in step 3.
kubectl exec -it inventory -n default -- /bin/bash


kubectl delete pod inventory


kubectl delete ns my-namespace



########
kubectl create namespace my-namespace
kubectl apply -f service.yaml

kubectl get pods --all-namespaces -o wide
kubectl get pods -n my-namespace
kubectl get all -n my-namespace

kubectl exec -it pod/my-deployment-675f769895-h28f5 -n my-namespace -- /bin/bash
kubectl exec -it pod/my-deployment-675f769895-949ld -n my-namespace -- /bin/bash
kubectl exec -it pod/my-deployment-675f769895-j7dk5 -n my-namespace -- /bin/bash




kubectl -n my-namespace port-forward inventory 8000:80


kubectl get svc  -n my-namespace