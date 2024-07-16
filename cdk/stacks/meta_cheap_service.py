from aws_cdk import Stack
from aws_cdk import aws_apigatewayv2 as apigatewayv2
from aws_cdk import aws_apigatewayv2_integrations as integrations
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as route53_targets
from aws_cdk import aws_servicediscovery as servicediscovery
from constructs import Construct
from stacks.meta_cheap_infra import MetaCheapInfraStack


class MetaCheapServiceStack(Stack):

    def __init__(
        self, scope: Construct, id: str, infra: MetaCheapInfraStack, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Get the existing resources
        # vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=VPC_ID)
        # hosted_zone = route53.HostedZone.from_lookup(
        #     self, "HostedZone", domain_name="whillas.com"
        # )
        # certificate = acm.Certificate.from_certificate_arn(
        #     self, "Certificate", certificate_arn="(link unavailable)"
        # )
        # vpc_link = apigatewayv2.VpcLink.from_vpc_link_arn(
        #     self, "VpcLink", vpc_link_arn="(link unavailable)"
        # )
        # cloud_map_namespace = servicediscovery.PrivateDnsNamespace.from_namespace_arn(
        #     self, "CloudMapNamespace", namespace_arn="(link unavailable)"
        # )

        # Create an ECS task definition
        task_definition = ecs.TaskDefinition(
            self,
            "TaskDefinition",
            cpu="256",
            memory_mib="512",
            family="my-task-definition",
        )

        # Create IAM roles for your ECS task definition
        task_definition_exec_role = iam.Role(
            self,
            "TaskDefinitionExecRole",
            assumed_by=iam.ServicePrincipal("(link unavailable)"),
        )
        task_definition_task_role = iam.Role(
            self,
            "TaskDefinitionTaskRole",
            assumed_by=iam.ServicePrincipal("(link unavailable)"),
        )

        # Create a CloudMap service
        cloud_map_service = infra.cloud_map_namespace.create_service(
            self, "CloudMapService", service_name="my-service"
        )

        # Create an ECS service
        ecs_service = ecs_patterns.Service(
            self,
            "ECSService",
            service_name="my-service",
            task_definition=task_definition,
            cluster=ecs.Cluster.from_cluster_arn(
                self, "ECSCluster", cluster_arn="(link unavailable)"
            ),
            desired_count=1,
            assign_public_ip=True,
            security_groups=["ECSServiceSecurityGroup"],
            cloud_map_options=ecs_patterns.CloudMapOptions(
                cloud_map_namespace=infra.cloud_map_namespace, service=cloud_map_service
            ),
        )

        # Create a security group for your ECS service
        ecs_service_security_group = ec2.SecurityGroup(
            self,
            "ECSServiceSecurityGroup",
            vpc=infra.vpc,
            description="ECS service security group",
        )
        ecs_service_security_group.add_ingress_rule(
            infra.vpc_link_security_group, ec2.Port.tcp(8080)
        )

        # Create an API gateway
        api_gateway = apigatewayv2.HttpApi(
            self,
            "ApiGateway",
            default_domain_name="(link unavailable)",
            certificate=infra.certificate,
            vpc_link=infra.vpc_link,
        )

        # Create an API gateway integration
        integration = integrations.HttpServiceIntegration(
            self,
            "Integration",
            service_name="my-service",
            namespace_name="example",
            vpc_link=infra.vpc_link,
        )

        # Create an API gateway route
        api_gateway.add_routes(
            self,
            "Route",
            routes=[
                apigatewayv2.HttpRoute(
                    path="/", methods=["GET"], integration=integration
                )
            ],
        )

        # Create an API gateway API mapping
        api_mapping = apigatewayv2.ApiMapping(
            self,
            "ApiMapping",
            api_id=api_gateway.api_id,
            domain_name="(link unavailable)",
            stage="prod",
        )

        # Create a Route 53 record
        route53.ARecord(
            self,
            "Route53Record",
            zone=infra.hosted_zone,
            record_name="farm2",
            target=route53.RecordTarget.from_alias(
                route53_targets.ApiGatewayDomain(api_gateway)
            ),
        )
