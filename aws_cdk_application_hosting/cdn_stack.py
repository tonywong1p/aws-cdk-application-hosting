from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_cloudfront as cloudfront
import aws_cdk.aws_cloudfront_origins as origins
import aws_cdk.aws_certificatemanager as acm
import aws_cdk.aws_route53 as route53


# Config
domain = "nlpoc.net"


class CdnStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, origin, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        hosted_zone = route53.HostedZone(self, "HostedZone",
                                            zone_name=domain
                                            )

        certificate = acm.DnsValidatedCertificate(self, "mySiteCert",
                                                     domain_name=f'www.{domain}',
                                                     hosted_zone=hosted_zone,
                                                     validation=acm.CertificateValidation.from_dns(hosted_zone)
                                                     )

        cloudfront.Distribution(self, "myDist",
                                default_behavior={
                                    "origin": origins.LoadBalancerV2Origin(origin)},
                                domain_names=[f'www.{domain}'],
                                certificate=certificate
                                )
