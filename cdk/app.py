#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from stacks.fat_lambda_stack import CdkStack
from stacks.django_ecs_stack import DjangoEcsStack

app = cdk.App()
DjangoEcsStack(
    app,
    "DjangoEcsStack",
    env=cdk.Environment(account="339454265489", region="ap-southeast-2"),
)

app.synth()
