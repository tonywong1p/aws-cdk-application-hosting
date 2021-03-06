from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_s3 as s3


class S3Stack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        bucket = s3.Bucket(self, "MyCDKBucket",
                           encryption=s3.BucketEncryption.KMS_MANAGED
                           )

        s3_endpoint = vpc.add_gateway_endpoint("S3Endpoint",
                                                      service=ec2.GatewayVpcEndpointAwsService.S3
                                                      )
