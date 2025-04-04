import boto3
import json
import bisect

s3 = boto3.client('s3')
BUCKET = 'thanya2guide'
KEY = 'results.txt'

cached_data = []  # Sorted list for binary search

def load_file():
    global cached_data
    if not cached_data:
        print("Loading data from S3...")
        response = s3.get_object(Bucket=BUCKET, Key=KEY)
        body = response['Body'].read().decode('utf-8')

        # Convert lines to integers & sort
        cached_data = sorted(
            int(line.strip()) for line in body.splitlines() if line.strip().isdigit()
        )

        print(f"Loaded {len(cached_data)} hallticket numbers.")

def binary_search(arr, target):
    index = bisect.bisect_left(arr, target)
    return index < len(arr) and arr[index] == target

def return_response(resp):
    print(f"Returning response: {resp}")
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(resp)
    }

def lambda_handler(event, context):
    load_file()
    print("EVENT RECEIVED:", json.dumps(event))

    try:
        # Parse input JSON safely
        if isinstance(event, dict) and 'body' in event:
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            print("Invalid event: Missing 'body'")
            return return_response({'error': 'Invalid request format'})

        print("Parsed body:", body)

        hallticket_raw = body.get('hallticket', None)

        if hallticket_raw is None:
            return return_response({'error': 'hallticket is required'})

        # Convert to string, strip, and ensure it’s a digit
        hallticket_str = str(hallticket_raw).strip()

        if not hallticket_str.isdigit():
            return return_response({'error': 'hallticket must be a number'})

        hallticket = int(hallticket_str)
        print(f"Checking hallticket: {hallticket}")

        if binary_search(cached_data, hallticket):
            print(f"Hallticket {hallticket} found")
            return return_response({'status': 'found'})
        else:
            print(f"Hallticket {hallticket} not found")
            return return_response({'status': 'not_found'})

    except Exception as e:
        print(f"Exception: {e}")
        return return_response({'error': 'Internal server error'})
