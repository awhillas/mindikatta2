from aws_cdk import aws_apigatewayv2 as apigwv2
from aws_cdk import aws_apigatewayv2_integrations as apigwv2_integrations
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets
from aws_cdk import aws_servicediscovery as servicediscovery
from aws_cdk import core
from constructs import Construct

from .cheap_stack_infra import CheapStackSharedInfra


class AppStack(core.Stack):

    def __init__(
        self,
        scope: Construct,
        id: str,
        infrastructure_stack: CheapStackSharedInfra,
        **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Get resources from the infrastructure stack
        vpc = infrastructure_stack.vpc
        hosted_zone = infrastructure_stack.hosted_zone
        certificate = infrastructure_stack.certificate
        vpc_link = infrastructure_stack.vpc_link
        cloud_map_namespace = infrastructure_stack.cloud_map_namespace

        # Define security group for the ECS service
        ecs_security_group = ec2.SecurityGroup(
            self,
            "EcsSecurityGroup",
            vpc=vpc,
            description="Allow traffic from API Gateway VPC Link",
            allow_all_outbound=True,
        )

        # Only allow requests from API Gateway security group
        ecs_security_group.add_ingress_rule(
            infrastructure_stack.security_group,
            ec2.Port.tcp(80),
            "Allow inbound HTTP traffic from API Gateway",
        )

        # Create ECS task definition using Fargate
        task_role = iam.Role(
            self,
            "TaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )

        task_definition = ecs.FargateTaskDefinition(
            self, "TaskDefinition", task_role=task_role, memory_limit_mib=512, cpu=256
        )

        container = task_definition.add_container(
            "AppContainer",
            image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
            logging=ecs.AwsLogDriver(stream_prefix="ecs"),
            health_check=ecs.HealthCheck(
                command=["CMD-SHELL", "curl -f http://localhost/ || exit 1"],
                interval=core.Duration.seconds(30),
                retries=3,
                start_period=core.Duration.minutes(1),
                timeout=core.Duration.seconds(5),
            ),
        )
        container.add_port_mappings(
            ecs.PortMapping(container_port=80, protocol=ecs.Protocol.TCP)
        )

        # Create a CloudMap service
        cloud_map_service = cloud_map_namespace.create_service(
            "AppService",
            dns_record_type=servicediscovery.DnsRecordType.A,
            dns_ttl=core.Duration.seconds(30),
        )

        # Create ECS service
        ecs_service = ecs.FargateService(
            self,
            "EcsService",
            cluster=ecs.Cluster(self, "EcsCluster", vpc=vpc),
            task_definition=task_definition,
            service_name="app-service",
            cloud_map_options=ecs.CloudMapOptions(
                cloud_map_namespace=cloud_map_namespace, name="app-service"
            ),
            security_groups=[ecs_security_group],
            desired_count=1,
        )

        # Create API Gateway integration for ECS service through VPC link
        http_api = apigwv2.HttpApi(
            self,
            "HttpApi",
            default_domain_mapping=apigwv2.DomainMappingOptions(
                domain_name=apigwv2.DomainName.from_domain_name_attributes(
                    self,
                    "ApiDomainName",
                    certificate_arn=certificate.certificate_arn,
                    domain_name=hosted_zone.zone_name,
                )
            ),
        )

        http_integration = apigwv2_integrations.HttpServiceIntegration(
            "ecsServiceIntegration",
            service=cloud_map_service,
            vpc_link=vpc_link,
            method=apigwv2.HttpMethod.ANY,
            api=http_api,
        )

        http_api.add_routes(path="/{proxy+}", integration=http_integration)

        # Create Route 53 record to make the API accessible
        route53.ARecord(
            self,
            "ApiGatewayAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.ApiGatewayv2Domain(http_api.api_endpoint)
            ),
            record_name="my-app",
        )
