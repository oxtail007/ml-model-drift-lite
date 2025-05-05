#!/usr/bin/env node
import * as cdk from 'aws-cdk-lib';
import { MlDriftLiteStack } from '../lib/ml_drift_lite-stack';

const app = new cdk.App();
new MlDriftLiteStack(app, 'MlDriftLiteStack');
