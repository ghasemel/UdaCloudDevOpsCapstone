aws iam create-role \
  --role-name myAmazonEKSCNIRole \
  --assume-role-policy-document file://"cni-role-trust-policy.json"



aws iam attach-role-policy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy \
  --role-name myAmazonEKSCNIRole


#Associate the Kubernetes service account used by the VPC CNI plugin to the IAM role. 867975079432 is your account ID.
aws eks update-addon \
  --cluster-name my-cluster \
  --addon-name vpc-cni \
  --service-account-role-arn arn:aws:iam::867975079432:role/myAmazonEKSCNIRole 