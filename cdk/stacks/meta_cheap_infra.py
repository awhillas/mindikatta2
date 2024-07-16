from aws_cdk import Stack
from aws_cdk import aws_apigatewayv2 as apigatewayv2
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct
from stacks import HOSTED_ZONE_ID, VPC_ID, DOMAIN_NAME


class MetaCheapInfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC
        self.vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=VPC_ID)

        # Create subnets
        self.subnet_a = ec2.Subnet(
            self,
            "SubnetA",
            vpc_id=self.vpc.vpc_id,
            cidr_block="10.1.1.0/24",
            availability_zone=f"{self.region}a",
        )

        self.subnet_b = ec2.Subnet(
            self,
            "SubnetB",
            vpc_id=self.vpc.vpc_id,
            cidr_block="10.1.2.0/24",
            availability_zone=f"{self.region}b",
        )

        # Create a Route 53 hosted zone
        self.hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "HostedZoneWhillasCom",
            hosted_zone_id=HOSTED_ZONE_ID,
            zone_name=DOMAIN_NAME,
        )

        # Create an ACM-managed TLS certificate
        self.certificate = acm.Certificate(
            self,
            "Certificate",
            domain_name="dev."+DOMAIN_NAME,
            validation=acm.CertificateValidation.from_dns(hosted_zone=self.hosted_zone),
        )

        # Create a security group for the VPC link
        self.vpc_link_security_group = ec2.SecurityGroup(
            self,
            "VpcLinkSecurityGroup",
            vpc=self.vpc,
            description="VPC link security group",
        )

        # Create an API Gateway VPC Link
        self.vpc_link = apigatewayv2.VpcLink(
            self,
            "VpcLink",
            vpc=self.vpc,
            security_groups=[self.vpc_link_security_group],
            subnets=ec2.SubnetSelection(subnets=[self.subnet_a, self.subnet_b]),
        )

        # Create a Cloud Map namespace
        self.cloud_map_namespace = servicediscovery.PrivateDnsNamespace(
            self, "CloudMapNamespace", vpc=self.vpc, name="whillas.com"
        )

        # Create a route table
        self.route_table = ec2.CfnRouteTable(self, "RouteTable", vpc_id=self.vpc.vpc_id)

        # Create a route
        ec2.CfnRoute(
            self,
            "InternetRoute",
            route_table_id=self.route_table.attr_route_table_id,
            destination_cidr_block="0.0.0.0/0",
            gateway_id=ec2.CfnInternetGateway(self, "InternetGateway"),
        )

        # Associate the subnets with the route table
        ec2.SubnetRouteTableAssociation(
            self,
            "RouteTableAssociationSubnetA",
            subnet_id=self.subnet_a,
            route_table_id=self.route_table.attr_route_table_id,
        )

        ec2.SubnetRouteTableAssociation(
            self,
            "RouteTableAssociationSubnetB",
            subnet_id=self.subnet_b,
            route_table_id=self.route_table.attr_route_table_id,
        )
