from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from constructs import Construct


class DjangoEc2Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Use an existing VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id="vpc-5a5f033d")

        # Create an EC2 instance using an Minimal Ubuntu 24.04 AMI
        instance = ec2.Instance(
            self,
            "K3sInstance",
            instance_type=ec2.InstanceType("t2.micro"),
            vpc=vpc,
            machine_image=ec2.MachineImage.lookup(
                # see https://documentation.ubuntu.com/aws/en/latest/aws-how-to/instances/find-ubuntu-images/
                name="/aws/service/marketplace/prod-umggziwlkgulc/latest"
            ),  # Ubuntu 24.04
        )

        # Create an ECR repository
        ecr_repository = ecr.Repository(
            self, "DjangoRepository", repository_name="mindikatta"
        )

        # Create an IAM role for the EC2 instance
        role = iam.Role(
            self, "MyEC2Role", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com")
        )

        # Grant the EC2 instance permissions to access the ECR repository
        ecr_repository.grant_pull_push(role)

        # Attach the IAM role to the EC2 instance
        instance.add_to_role_policy(
            iam.PolicyStatement(actions=["ecr:GetAuthorizationToken"], resources=["*"])
        )
        instance.add_to_role_policy(
            iam.PolicyStatement(
                actions=[
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:GetDownloadUrlForLayer",
                    "ecr:GetRepositoryPolicy",
                    "ecr:DescribeRepositories",
                    "ecr:ListImages",
                    "ecr:DescribeImages",
                    "ecr:BatchGetImage",
                    "ecr:InitiateLayerUpload",
                    "ecr:UploadLayerPart",
                    "ecr:CompleteLayerUpload",
                    "ecr:PutImage",
                ],
                resources=[ecr_repository.repository_arn],
            )
        )

        # Create a Route 53 record set for the subdomain
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "WhillasComHostedZone",
            hosted_zone_id="Z0388674QNPI26RBI85C",
            zone_name="whillas.com",
        )
        record_set = route53.RecordSet(
            self,
            "RecordSet",
            zone=hosted_zone,
            record_name="mindikatta",  # Subdomain
            record_type="A",
            target=route53_targets.InstanceTarget(instance),
        )
