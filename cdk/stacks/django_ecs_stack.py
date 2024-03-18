import os

from aws_cdk import Duration, RemovalPolicy, Stack
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from constructs import Construct
from dotenv import load_dotenv
from stacks import HOSTED_ZONE_ID, VPC_ID

load_dotenv()


class DjangoEcsStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get the existing VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=VPC_ID)

        # Create a public subnet group
        public_subnet_group = ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster", vpc=vpc)

        # Create an ECR repository
        ecr_repository = ecr.Repository(self, "EcrRepository")

        # Build the Docker image from the local directory
        image = ecs.ContainerImage.from_asset("..")

        # Create a Fargate task definition
        task_definition = ecs.FargateTaskDefinition(
            self,
            "TaskDefinition",
            memory_limit_mib=512,
            cpu=256,
        )

        # Add a container to the task definition
        container = task_definition.add_container(
            "DjangoContainer",
            image=image,
            port_mappings=[ecs.PortMapping(container_port=8000)],
            environment={
                "DATABASE_URL": os.getenv("DATABASE_URL"),
                "DJANGO_DEBUG": "True",  # should be False for production
                "DJANGO_SETTINGS_MODULE": "config.production",
            },
            logging=ecs.LogDrivers.aws_logs(
                stream_prefix="DjangoContainer",
                log_group=logs.LogGroup(
                    self,
                    "LogGroup",
                    retention=logs.RetentionDays.ONE_MONTH,
                    removal_policy=RemovalPolicy.DESTROY,
                ),
            ),
        )

        # Create a Fargate service
        fargate_service = ecs.FargateService(
            self,
            "FargateService",
            cluster=cluster,
            task_definition=task_definition,
            desired_count=1,
            assign_public_ip=True,
        )

        # Create an Application Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self,
            "ALB",
            vpc=vpc,
            internet_facing=True,
        )

        # Add a listener to the ALB
        listener = alb.add_listener("Listener", port=80)

        # Create a target group for the ALB
        target_group = listener.add_targets(
            "TargetGroup",
            port=80,
            targets=[fargate_service],
            health_check=elbv2.HealthCheck(
                path="/api/",
                enabled=True,
                healthy_http_codes="200",
                timeout=Duration.seconds(5),
            ),
        )

        # Create a certificate for the domain
        certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name="farm.whillas.com",
            validation=acm.CertificateValidation.from_dns(),
        )

        # Add HTTPS listener to the ALB
        https_listener = alb.add_listener(
            "HttpsListener",
            port=443,
            certificates=[certificate],
            default_action=elbv2.ListenerAction.forward([target_group]),
        )

        # Get the existing hosted zone
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZone",
            hosted_zone_id=HOSTED_ZONE_ID,
            zone_name="whillas.com",
        )

        # Create an A record for the subdomain
        route53.ARecord(
            self,
            "ARecord",
            zone=hosted_zone,
            record_name="farm",
            target=route53.RecordTarget.from_alias(
                route53_targets.LoadBalancerTarget(alb)
            ),
        )
