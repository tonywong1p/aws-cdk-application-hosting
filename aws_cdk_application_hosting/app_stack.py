from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.aws_autoscaling as autoscaling

with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class AppStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        alb = elbv2.ApplicationLoadBalancer(self, "ALB",
                                            vpc=vpc,
                                            internet_facing=True
                                            )
        listener = alb.add_listener("Listener",
                                    port=80,
                                    open=True
                                    )

        security_group = ec2.SecurityGroup(self, "SecurityGroup",
                                           vpc=vpc,
                                           description="Allow access to ec2 instances",
                                           allow_all_outbound=True
                                           )
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(
            80), "allow HTTP access from the world")
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(
            22), "allow ssh access from the world")

        asg = autoscaling.AutoScalingGroup(self, "ASG",
                                           vpc=vpc,
                                           instance_type=ec2.InstanceType(
                                               "t3.small"),
                                           machine_image=ec2.MachineImage.generic_linux({
                                               "ap-east-1": "ami-0312f467545f742c4"
                                           }),
                                           min_capacity=2,
                                           max_capacity=5,
                                           security_group=security_group,
                                        #    block_devices=[autoscaling.BlockDevice(
                                        #        device_name="EBSApp",
                                        #        volume=autoscaling.BlockDeviceVolume.ebs(20,
                                        #                                                 encrypted=True
                                        #                                                 )
                                        #    )]
                                           )
        asg.scale_on_cpu_utilization("KeepSpareCPU",
                                     target_utilization_percent=70
                                     )

        group = listener.add_targets("ApplicationFleet",
                                     port=80,
                                     targets=[asg]
                                     )

        # Output
        core.CfnOutput(self, "Output",
                       value=alb.load_balancer_dns_name)
        self.security_group = security_group
        self.alb = alb
