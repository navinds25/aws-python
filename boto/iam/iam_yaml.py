import boto3
import yaml

with open('users.yml') as f:
    config = yaml.safe_load(f)

print(config)

for usertype in config['users']:
    print("usertype: {}".format(usertype))
    for username in config['users'][usertype]:
        userpath = "/{}".format(usertype)
        print("path: {}, username: {}, permission_boundaries: {}".format(userpath, username, config['users'][usertype][username]['permission_boundary']))
