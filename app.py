#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk_application_hosting.vpc_stack import VpcStack
from aws_cdk_application_hosting.app_tier_stack import AppTierStack


app = core.App()

vpc_stack = VpcStack(app,"cdk-vpc")
app_tier_stack = AppTierStack(app, "cdk-app-tier", vpc=vpc_stack.vpc)

app.synth()
