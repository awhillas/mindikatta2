from aws_cdk import Stack
from aws_cdk import aws_apigatewayv2 as apigatewayv2
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct
from stacks import HOSTED_ZONE_ID, VPC_ID


class CheapStackSharedInfra(Stack):
    """
    Shared infrastructure for the CheapStack
    See: https://awsteele.com/blog/2022/10/15/cheap-serverless-containers-using-api-gateway.html
    """

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        """Genrated using GPT-4o"""
        super().__init__(scope, id, **kwargs)

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(self, "ImportedVPC", vpc_id=VPC_ID)

        # Import existing Route 53 Hosted Zone
        hosted_zone = route53.HostedZone.from_hosted_zone_id(
            self, "ImportedHostedZone", hosted_zone_id=HOSTED_ZONE_ID
        )

        # Create an ACM-managed TLS certificate
        certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name=hosted_zone.zone_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone),
        )

        # Create a security group for the API Gateway vpc link
        security_group = ec2.SecurityGroup(
            self,
            "ApiGatewaySecurityGroup",
            vpc=vpc,
            description="Security group for API Gateway VPC Link",
            allow_all_outbound=True,
        )

        # Allow inbound traffic for API Gateway
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow inbound HTTP traffic"
        )
        security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(), ec2.Port.tcp(443), "Allow inbound HTTPS traffic"
        )

        # Create an API Gateway VPC Link
        vpc_link = apigatewayv2.VpcLink(
            self,
            "VpcLink",
            vpc=vpc,
            vpc_link_name="MyVpcLink",
            security_groups=[security_group],
        )

        # Create a Cloud Map namespace
        cloud_map_namespace = servicediscovery.PrivateDnsNamespace(
            self, "CloudMapNamespace", name="my-namespace.local", vpc=vpc
        )

        # Save these here (export) so we can pass in this shared infra to other stacks

        self.vpc = vpc
        self.hosted_zone = hosted_zone
        self.certificate = certificate
        self.security_group = security_group
        self.vpc_link = vpc_link
        self.cloud_map_namespace = cloud_map_namespace
