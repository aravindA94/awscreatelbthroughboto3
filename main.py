# Author : Aravind Ashok
# The Following Code Creates a Load Balancer, Target Group, and Registers the EC2 Instaces
import boto3

#Globals 
web01ID = ''
web02ID = ''
web03ID = ''

vpcID =''
publicSubnetOne = ''
publicSubnetTwo = ''
publicSubnetThree = ''

elbSecurityGroup = ''


loadBalancer = boto3.client('elbv2',aws_access_key_id='', aws_secret_access_key='', region_name="us-east-2")

createLoadBalancerResponse = loadBalancer.create_load_balancer(
        Name='aravind-demo-elb',
        Subnets=[publicSubnetOne, publicSubnetTwo, publicSubnetThree],
        SecurityGroups=[elbSecurityGroup],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
loadBalancerARN = createLoadBalancerResponse['LoadBalancers'][0]['LoadBalancerArn']
print(f'The Application load balancer has been successfully created!! ----- ARN: {loadBalancerARN}')


createTargetGroupResponse = loadBalancer.create_target_group(
        Name='aravind-demo-target-group',
        Protocol='HTTP',
        Port=80,
        TargetType='instance',
        HealthCheckPath='/index.html',
        VpcId=vpcID
    )


targetGroupID = createTargetGroupResponse['TargetGroups'][0]['TargetGroupArn']
print(f'Created Target Group: created target group {targetGroupID}')

listnerId = loadBalancer.create_listener(
    LoadBalancerArn=loadBalancerARN,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[
        {
            'Type': 'forward',
            'TargetGroupArn': targetGroupID
        },
    ]
)

# Register web instances with web-elb
regis_targets = loadBalancer.register_targets(TargetGroupArn=targetGroupID,Targets=[{'Id': web01ID,'Port': 80},{'Id': web02ID,'Port': 80},{'Id': web03ID,'Port': 80}])