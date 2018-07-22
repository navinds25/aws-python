#!/usr/bin/env python
''' 
This script is for generating AMIs on AWS.
Prequisites:
1. It requires are an ova format virtual image that can be generated via virtualbox. 
2. Requires configuration of user crendentials. (via aws configure, ie. awscli)
3. Requires AWS IAM setup with vmimport role.

'''
import boto3

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')

def upload_ova_image(bucket_name, filename, key_name):
    ''' Creates S3 bucket and upload image to the bucket'''
    bucket_info = s3.create_bucket(ACL='private', Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-south-1'})
    # Need to change access rights to bucket.
    s3.upload_file(filename, bucket_name, key_name)
    #Above command can be replaced as multipart upload.
    return bucket_info


if __name__ == '__main__':
    upload_ova_image('centos7amis', '../AMIs/ExportedVMs/Centos7.ova', 'Centos7v1')

disk_containers=[{'Description': 'Centos7v1', 'Format': 'ova', 'UserBucket': {'S3Bucket': 'centos7amis', 'S3Key': 'Centos7v1'}}]

ec2.import_image(Architecture='x86_64', Description='Centos7v1', DiskContainers=disk_containers)
