import boto3
import sys
import json
import logging as log

log.basicConfig(level='INFO')

with open('users.json') as f:
    config = json.load(f)

iam = boto3.client('iam')

def get_policy_info(client, policy_name):
    all_policies = client.list_policies(Scope='All')
    policies = all_policies['Policies']
    responses = []
    for policy in policies:
        if policy['PolicyName'] == policy_name:
            responses.append(policy)
    if len(responses) > 1:
        log.error("More than 1 policy exists with given name")
        sys.exit(1)
    if not responses:
        log.error("Could not find policy with provided name")
        sys.exit(1)
    return responses[0]

def create_users(client, config):
    users = config['Users']
    responses = []
    for usertype in users:
        for username in users[usertype]:
            userpath = "/{}/".format(usertype.lower())
            permissions_boundary = users[usertype][username]['PermissionsBoundary']
            permissions_boundary_arn = get_policy_info(client, permissions_boundary)['Arn']
            log.info("Creating user: UserName: {}, Path: {}, PermissionsBoundary: {}".format(
                username,
                userpath,
                permissions_boundary_arn
                ))
            resp = client.create_user(
                Path=userpath,
                UserName=username,
                PermissionsBoundary=permissions_boundary_arn)
            responses.append(resp)
    return responses

def delete_policy_by_name(client, policy_name):
    for policy in get_policy_info(client, policy_name):
        log.info('Deleting policy: {}'.format(policy))
        client.delete_policy(PolicyArn=policy['Arn'])

def create_pb_policies(client, config):
    ''' Creates all permission boundary policies from config '''
    pb_policies = config['Policies']['PermissionsBoundary']
    responses = []
    for policy in pb_policies:
        log.info("Creating policy {} with \
            path: {} ; \
            policydocument: {} ; \
            description: {}".format(
            policy,
            pb_policies[policy]['path'],
            pb_policies[policy]['policydoc'],
            pb_policies[policy]['description']
        ))
        resp = client.create_policy(PolicyName=policy,
            Path=pb_policies[policy]['path'],
            PolicyDocument=json.dumps(pb_policies[policy]['policydoc']),
            Description=pb_policies[policy]['description'])
        responses.append(resp)
    return responses

if __name__ == '__main__':
    resp = create_pb_policies(iam, config)
    log.info(resp)
    resp = create_users(iam, config)
    log.info(resp)
