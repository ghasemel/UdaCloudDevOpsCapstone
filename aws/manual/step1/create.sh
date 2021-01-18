aws cloudformation create-stack \
  --stack-name $1 \
  --template-body file://"$2" \
  --region=us-west-2
# ./create.sh UdacityCapstoneProject network.yml network-param.json

./create.sh eks-network eks-network.yaml

 #aws ec2 describe-availability-zones \
 #--query "AvailabilityZones[?(RegionName=='us-west-1')].[AvailabilityZones]"

#aws ec2 create-default-subnet --availability-zone 	us-west-2d