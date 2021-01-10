aws cloudformation create-stack \
  --stack-name $1 \
  --template-body file://$2  \
  --parameters file://$3 \
  --capabilities "CAPABILITY_IAM" "CAPABILITY_NAMED_IAM" \
  --region=us-west-2
# ./create.sh UdacityCapstoneProject network.yml network-param.json

 #aws ec2 describe-availability-zones \
 #--query "AvailabilityZones[?(RegionName=='us-west-1')].[AvailabilityZones]"

#aws ec2 create-default-subnet --availability-zone 	us-west-2d