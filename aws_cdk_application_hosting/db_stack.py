from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class DbStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        source_instance = rds.DatabaseInstance(self, "Instance",
                                               engine=rds.DatabaseInstanceEngine.mysql(
                                                   version=rds.MysqlEngineVersion.VER_8_0_19
                                               ),
                                               instance_type=ec2.InstanceType.of(
                                                   ec2.InstanceClass.MEMORY5, ec2.InstanceSize.LARGE),
                                               allocated_storage=100,
                                               multi_az=True,
                                               vpc=vpc,
                                               vpc_subnets={
                                                   "subnet_type": ec2.SubnetType.PRIVATE
                                               },
                                               publicly_accessible=False,
                                               storage_encrypted=True,
                                               )

        # core.CfnOutput(self, "Bastion Host Public IP",
        #                value=host.instance_public_ip)
        # self.vpc = vpc
