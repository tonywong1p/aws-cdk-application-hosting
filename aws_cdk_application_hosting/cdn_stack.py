from aws_cdk import (
    core,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    aws_wafv2 as waf
)


# Configurations
domain = "nlpoc.net"
# Create a hosted zone with correct name server
hosted_zone_id = "Z04270622ITEOORZ9V5FH"
# Create a cert in us-east-1
acm_arn = "arn:aws:acm:us-east-1:290455323267:certificate/a849184d-5828-4e34-9d49-4dddd28f723e"


class CdnStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, origin, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # web_acl = waf.CfnWebACL(self, "WAF ACL",
        #                         default_action={"allow": {}},
        #                         scope="GLOBAL",
        #                         visibility_config={
        #                             "sampledRequestsEnabled": True,
        #                             "cloudWatchMetricsEnabled": True,
        #                             "metricName": "web-acl",
        #                         },
        #                         rules=[
        #                             {
        #                                 "name": "rate_limit_500",
        #                                 "priority": 0,
        #                                 "action": {
        #                                     "block": {}
        #                                 },
        #                                 "visibilityConfig": {
        #                                     "sampledRequestsEnabled": True,
        #                                     "cloudWatchMetricsEnabled": True,
        #                                     "metricName": "rate_limit_500"
        #                                 },
        #                                 "statement": {
        #                                     "rateBasedStatement": {
        #                                         "limit": 500,
        #                                         "aggregateKeyType": "IP"
        #                                     }
        #                                 }
        #                             },
        #                             {
        #                                 "priority": 1,
        #                                 "overrideAction": {"none": {}},
        #                                 "visibilityConfig": {
        #                                     "sampledRequestsEnabled": True,
        #                                     "cloudWatchMetricsEnabled": True,
        #                                     "metricName": "AWS-AWSManagedRulesAmazonIpReputationList",
        #                                 },
        #                                 "name": "AWS-AWSManagedRulesAmazonIpReputationList",
        #                                 "statement": {
        #                                     "managedRuleGroupStatement": {
        #                                         "vendorName": "AWS",
        #                                         "name": "AWSManagedRulesAmazonIpReputationList",
        #                                     },
        #                                 },
        #                             },
        #                             {
        #                                 "priority": 2,
        #                                 "overrideAction": {"none": {}},
        #                                 "visibilityConfig": {
        #                                     "sampledRequestsEnabled": True,
        #                                     "cloudWatchMetricsEnabled": True,
        #                                     "metricName": "AWS-AWSManagedRulesCommonRuleSet",
        #                                 },
        #                                 "name": "AWS-AWSManagedRulesCommonRuleSet",
        #                                 "statement": {
        #                                     "managedRuleGroupStatement": {
        #                                         "vendorName": "AWS",
        #                                         "name": "AWSManagedRulesCommonRuleSet",
        #                                     },
        #                                 },
        #                             },
        #                             {
        #                                 "priority": 3,
        #                                 "overrideAction": {"none": {}},
        #                                 "visibilityConfig": {
        #                                     "sampledRequestsEnabled": True,
        #                                     "cloudWatchMetricsEnabled": True,
        #                                     "metricName": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
        #                                 },
        #                                 "name": "AWS-AWSManagedRulesKnownBadInputsRuleSet",
        #                                 "statement": {
        #                                     "managedRuleGroupStatement": {
        #                                         "vendorName": "AWS",
        #                                         "name": "AWSManagedRulesKnownBadInputsRuleSet",
        #                                     },
        #                                 },
        #                             },
        #                             {
        #                                 "priority": 4,
        #                                 "overrideAction": {"none": {}},
        #                                 "visibilityConfig": {
        #                                     "sampledRequestsEnabled": True,
        #                                     "cloudWatchMetricsEnabled": True,
        #                                     "metricName": "AWS-AWSManagedRulesSQLiRuleSet",
        #                                 },
        #                                 "name": "AWS-AWSManagedRulesSQLiRuleSet",
        #                                 "statement": {
        #                                     "managedRuleGroupStatement": {
        #                                         "vendorName": "AWS",
        #                                         "name": "AWSManagedRulesSQLiRuleSet",
        #                                     },
        #                                 },
        #                             }
        #                         ]
        #                         )

        certificate = acm.Certificate.from_certificate_arn(
            self, "Certificate", acm_arn)

        distribution = cloudfront.Distribution(self, "myDist",
                                               default_behavior={
                                                   "origin": origins.LoadBalancerV2Origin(origin, protocol_policy=cloudfront.OriginProtocolPolicy.MATCH_VIEWER),
                                                   "viewer_protocol_policy": cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                                                   "cache_policy": cloudfront.CachePolicy(self, "myCachePolicy",
                                                                                          cache_policy_name="MyPolicy",
                                                                                          comment="A default policy",
                                                                                          default_ttl=core.Duration.minutes(
                                                                                              0),
                                                                                          min_ttl=core.Duration.minutes(
                                                                                              0),
                                                                                          max_ttl=core.Duration.minutes(
                                                                                              5),
                                                                                          )
                                               },
                                               domain_names=[f'www.{domain}'],
                                               certificate=certificate,
                                               # web_acl_id=web_acl.attr_arn
                                               )

        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(self, "MyZone",
                                                                     zone_name=domain,
                                                                     hosted_zone_id=hosted_zone_id
                                                                     )

        route53.ARecord(self, "Alias",
                        zone=hosted_zone,
                        target=route53.RecordTarget.from_alias(
                            targets.CloudFrontTarget(distribution)),
                        record_name=f'www.{domain}',
                        ttl=core.Duration.minutes(5)
                        )
