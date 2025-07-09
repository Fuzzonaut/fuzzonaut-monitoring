import json
import urllib3
import time
import boto3

cloudwatch = boto3.client('cloudwatch')
sns = boto3.client('sns')
http = urllib3.PoolManager()

def lambda_handler(event, context):
    url = "https://fuzzonaut.me"
    namespace = "Fuzzonaut/Health"
    
    try:
        start_time = time.time()
        response = http.request("GET", url)
        duration = time.time() - start_time

        print("Status code:", response.status)
        print("Response time (s):", duration)

        # Send custom metrics to CloudWatch
        cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': 'WebsiteAvailable',
                    'Value': 1 if response.status == 200 else 0,
                    'Unit': 'Count'
                },
                {
                    'MetricName': 'WebsiteLatency',
                    'Value': duration,
                    'Unit': 'Seconds'
                }
            ]
        )

        if response.status != 200:
            sns.publish(
                TopicArn="arn:aws:sns:us-east-1:050284120903:EC2AlarmNotifications",
                Subject="🚨 fuzzonaut.me returned error",
                Message=f"Website returned status code {response.status}"
            )

    except Exception as e:
        print("Exception occurred:", str(e))

        # Site unreachable — set availability = 0
        cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': 'WebsiteAvailable',
                    'Value': 0,
                    'Unit': 'Count'
                }
            ]
        )

        # Also alert
        sns.publish(
            TopicArn="arn:aws:sns:us-east-1:050284120903:EC2AlarmNotifications",
            Subject="🚨 fuzzonaut.me check FAILED",
            Message=f"Exception: {str(e)}"
        )
