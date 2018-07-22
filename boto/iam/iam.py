import boto3
import json

with open('users.json') as f:
    config = json.load(f)

iam = boto3.client('iam')

def create_users(client, config):
    users = config['Users']
    responses = []
    for usertype in users:
        for username in users[usertype]:
            userpath = "/{}/".format(usertype.lower())
            permission_boundary = users[usertype][username]['PermissionBoundary']
            print("Creating user: UserName: {}, Path: {}, PermissionBoundary: {}".format(username, userpath, permission_boundary))
            #resp = client.create_user(Path=userpath, UserName=username, PermissionsBoundary=permission_boundary)
            #responses.append(resp)
    return responses

def delete_policy_by_name(client, policy_name):
    all_policies = client.list_policies(Scope='All')
    policies = all_policies['Policies']
    for i in policies:
        if policies[i]['PolicyName'] == policy_name:
            print('Deleting policy: {}'.format(policies[i]))
            client.delete_policy(PolicyArn=policies[i]['Arn'])

if __name__ == '__main__':
    create_users(iam, config)
