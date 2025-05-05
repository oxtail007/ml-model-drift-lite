import { Stack, StackProps, Duration } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as events from 'aws-cdk-lib/aws-events';
import * as targets from 'aws-cdk-lib/aws-events-targets';
import * as iam from 'aws-cdk-lib/aws-iam';

export class MlDriftLiteStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const dataBucket = new s3.Bucket(this, 'DriftDataBucket');

    const driftFunction = new lambda.Function(this, 'DriftDetectionFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset('../mldrift'),
      handler: 'lambda_handler.handler',
      timeout: Duration.minutes(5),
      environment: {
        'BUCKET_NAME': dataBucket.bucketName
      }
    });

    dataBucket.grantRead(driftFunction);

    const rule = new events.Rule(this, 'DriftScheduleRule', {
      schedule: events.Schedule.rate(Duration.hours(1)),
    });

    rule.addTarget(new targets.LambdaFunction(driftFunction));

    driftFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: ['s3:GetObject'],
      resources: [`${dataBucket.bucketArn}/*`],
    }));
  }
}
