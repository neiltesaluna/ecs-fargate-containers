from aws_cdk import (core as cdk, aws_ecs_patterns, aws_ec2, aws_ecs, aws_elasticloadbalancingv2)


# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class EcsWebsiteStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecs_vpc = aws_ec2.Vpc(self, "EcsVPC", max_azs=2)    # minimum number of AZs is 2 for this stack to deploy
        ecs_vpc.apply_removal_policy(cdk.RemovalPolicy.DESTROY)

        ecs_cluster = aws_ecs.Cluster(
            self, "EcsCluster",
            vpc=ecs_vpc
        )

        ecs_taskdefinition = aws_ecs.FargateTaskDefinition(self, "EcsTaskDefinition")

        ecs_taskdefinition.add_container("ecsContainer",
            image=aws_ecs.ContainerImage.from_registry('coderaiser/cloudcmd:latest'),   # change image here
            cpu=256,
            memory_limit_mib=512,
            port_mappings=[aws_ecs.PortMapping(container_port=8000)]    # container port used for the image
        )

        ecs_fargate_service = aws_ecs.FargateService(
            self, "FargateService", 
            cluster=ecs_cluster,
            task_definition=ecs_taskdefinition
        )

        ecs_application_lb = aws_elasticloadbalancingv2.ApplicationLoadBalancer(
            self, "EcsAlb",
            vpc=ecs_vpc,
            internet_facing=True
        )

        alb_listener = ecs_application_lb.add_listener("AlbListener", port=80)

        ecs_tg = alb_listener.add_targets("EcsTG",
            port=80,
            targets=[ecs_fargate_service.load_balancer_target(
                container_name="ecsContainer",
                container_port=8000     # container port used for the image
            )]
        )

        cdk.CfnOutput(
            self, "WebUrl",
            description="URL from the load balancer",
            value=f"http://{ecs_application_lb.load_balancer_dns_name}/"
        )