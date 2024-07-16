#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from stacks.fat_lambda_stack import CdkStack
from stacks.django_ecs_stack import DjangoEcsStack
from stacks.meta_cheap_infra import MetaCheapInfraStack

env = cdk.Environment(account="339454265489", region="ap-southeast-2")
app = cdk.App()

DjangoEcsStack(
    app,
    "DjangoEcsStack",
    env=env,
)

infra = MetaCheapInfraStack(
    app,
    "MetaCheapInfraStack",
    env=env,
)

app.synth()
