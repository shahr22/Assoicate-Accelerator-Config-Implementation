import boto3
import json

BAD_PERMISSIONS = [
{
    "IpProtocol" : "tcp",
    "FromPort" : 0,
    "ToPort" : 65535,
    "UserIdGroupPairs" : [],
    "IpRanges" : [{"CidrIp" : "0.0.0.0/0"}],
    "PrefixListIds" : [],
    "Ipv6Ranges" : []
},
{
    'IpProtocol': '-1', 
    'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 
    'Ipv6Ranges': [], 
    'PrefixListIds': [], 
    'UserIdGroupPairs': []
    
}
]

def handler(event, context):
    group_id = event['Records'][0]['Sns']["Message"]
    client = boto3.client("ec2")
    group_descriptions = client.describe_security_groups(GroupIds=[group_id])
    ip_permissions = group_descriptions["SecurityGroups"][0]["IpPermissions"]
    print(ip_permissions)
    revoke_permissions = [item for item in ip_permissions if item in BAD_PERMISSIONS]
    if revoke_permissions:
        client.revoke_security_group_ingress(GroupId=group_id, IpPermissions=revoke_permissions)