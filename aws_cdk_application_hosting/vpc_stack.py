from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class VpcStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc(self, "VPC",
                      cidr="10.0.0.0/21",
                      max_azs=3,
                      nat_gateways=1,
                      subnet_configuration=[
                          ec2.SubnetConfiguration(
                              subnet_type=ec2.SubnetType.PUBLIC,
                              name="Ingress",
                              cidr_mask=24
                          ),
                          ec2.SubnetConfiguration(
                              subnet_type=ec2.SubnetType.PRIVATE,
                              name="Application",
                              cidr_mask=24,
                          ),
                          ec2.SubnetConfiguration(
                              subnet_type=ec2.SubnetType.ISOLATED,
                              name="Database",
                              cidr_mask=28,
                              reserved=True
                          )
                      ]
                      )

        host = ec2.BastionHostLinux(self, "cdk-vpc-BastionHost",
                                    vpc=vpc,
                                    subnet_selection=ec2.SubnetSelection(
                                          subnet_type=ec2.SubnetType.PUBLIC),
                                    # block_devices=[ec2.BlockDevice(
                                    #     device_name="EBSBastionHost_CDK",
                                    #     volume=ec2.BlockDeviceVolume.ebs(30,
                                    #                                      encrypted=True,
                                    #                                      delete_on_termination=True
                                    #                                      )
                                    # )]
                                    )

        core.CfnOutput(self, "Bastion Host Public IP",
                       value=host.instance_public_ip)
        self.vpc = vpc
