import os

from aws_cdk import Duration, Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk.aws_logs import RetentionDays
from constructs import Construct
from dotenv import load_dotenv

load_dotenv()


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Specify your hosted zone ID
        hosted_zone_id = "Z0388674QNPI26RBI85C"

        # Specify the subdomain name
        subdomain_name = "farm.whillas.com"

        # Get the hosted zone
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZone",
            hosted_zone_id=hosted_zone_id,
            zone_name="whillas.com",
        )

        # Create a certificate for the subdomain
        certificate = acm.Certificate(
            self,
            "SubdomainCertificate",
            domain_name=subdomain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )
        # Create a Lambda function
        # Create a Lambda function from a Dockerfile
        lambda_function = lambda_.DockerImageFunction(
            self,
            "LambdaFunction",
            code=lambda_.DockerImageCode.from_image_asset(
                directory="..",
                file="Dockerfile",
            ),
            timeout=Duration.minutes(15),
            log_retention=RetentionDays.ONE_MONTH,
            environment={
                "DATABASE_URL": os.getenv("DATABASE_URL"),
                "DJANGO_DEBUG": "True",  # should be False for production
                "DJANGO_SETTINGS_MODULE": "config.production",
            },
        )

        # Create an API Gateway REST API
        api = apigw.LambdaRestApi(
            self,
            "ApiGateway",
            handler=lambda_function,
            domain_name=apigw.DomainNameOptions(
                domain_name=subdomain_name,
                certificate=certificate,
            ),
        )

        # Create an A record for the subdomain
        route53.ARecord(
            self,
            "SubdomainARecord",
            record_name=subdomain_name,
            target=route53.RecordTarget.from_alias(targets.ApiGateway(api)),
            zone=hosted_zone,
        )
