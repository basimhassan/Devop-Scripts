import boto3
import json

# Specify your AWS region here
aws_region = " youregionname"

# Initialize a boto3 client with the specified region
client = boto3.client('secretsmanager', region_name=aws_region)

# Function to update an existing secret
def update_secret(secret_name, new_values):
    try:
        # Retrieve the current secret value
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        
        # Check if the secret value is in JSON format
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            
            # Check if the secret value is a valid JSON string
            try:
                secret_dict = json.loads(secret)
            except json.JSONDecodeError as e:
                return f"Error updating {secret_name}: Secret value is not a valid JSON string: {str(e)}"
        else:
            return f"Error updating {secret_name}: Secret is not in string format."
        
        # Update the secret with new values
        secret_dict.update(new_values)
        
        # Update the secret in Secrets Manager
        update_secret_response = client.update_secret(SecretId=secret_name, SecretString=json.dumps(secret_dict))
        
        # Check if the update was successful
        if 'ResponseMetadata' in update_secret_response and 'HTTPStatusCode' in update_secret_response['ResponseMetadata'] and update_secret_response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return f"Successfully updated {secret_name}"
        else:
            return f"Error updating {secret_name}: {update_secret_response}"
    except Exception as e:
        return f"Error updating {secret_name}: {str(e)}"

# Define your services and their new values here
services_to_update = {
   
    'Envname/service/microservicename':{}


}

# Iterate over each service and update
for secret_name, new_values in services_to_update.items():
    print(update_secret(secret_name, new_values))
