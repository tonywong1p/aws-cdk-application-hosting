#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk_application_hosting.vpc_stack import VpcStack
from aws_cdk_application_hosting.app_stack import AppStack
from aws_cdk_application_hosting.db_stack import DbStack
from aws_cdk_application_hosting.s3_stack import S3Stack
from aws_cdk_application_hosting.cdn_stack import CdnStack



app = core.App()

vpc_stack = VpcStack(app,"cdk-vpc")
app_stack = AppStack(app, "cdk-app", vpc=vpc_stack.vpc)
db_stack = DbStack(app, "cdk-db", vpc=vpc_stack.vpc)
s3_stack = S3Stack(app, "cdk-s3", vpc=vpc_stack.vpc)
cdn_stack = CdnStack(app, "cdk-cdn", origin=app_stack.alb)

app.synth()
