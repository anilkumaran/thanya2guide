import boto3
import json

s3 = boto3.client('s3')
BUCKET = 'thanya2guide'
KEY = '2025_tgcet_5th_class_results.json'

cached_data = {}

def load_file():
    global cached_data
    if cached_data:
        return

    print("🔄 Loading results file from S3...")
    response = s3.get_object(Bucket=BUCKET, Key=KEY)
    body = response['Body'].read().decode('utf-8')
    parsed = json.loads(body)

    # If the JSON is a dictionary with halltickets as keys
    if isinstance(parsed, dict):
        cached_data.update(parsed)
        print(f"✅ Loaded {len(cached_data)} students (dict format).")
        return

    # If the JSON is a list of rows
    elif isinstance(parsed, list):
        print("🔎 JSON is a list. Extracting hallticket field...")
        for record in parsed:
            hall_keys = [k for k in record.keys() if 'hall' in k.lower()]
            if not hall_keys:
                continue
            key = hall_keys[0]
            hallticket = str(record[key]).strip()
            cached_data[hallticket] = record
        print(f"✅ Loaded {len(cached_data)} students (list format).")
    else:
        print("❌ Invalid format. Expecting dict or list of dicts.")

def return_response(resp):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Methods': 'POST, OPTIONS'
        },
        'body': json.dumps(resp)
    }

def lambda_handler(event, context):
    load_file()
    print("📥 Incoming event:", event)

    # Support both direct and API Gateway invoke
    if 'body' in event:
        try:
            body = json.loads(event['body'])
        except Exception as e:
            print("❌ Error parsing body:", e)
            return return_response({'status': 'invalid_json'})
    else:
        body = event

    hallticket = str(body.get('hallticket', '')).strip()

    if not hallticket:
        return return_response({'status': 'invalid_input', 'message': 'Hallticket is required'})

    student = cached_data.get(hallticket)

    if student:
        print(f"✅ Hallticket {hallticket} found.")
        return return_response({
            'status': 'found',
            'student': student
        })
    else:
        print(f"❌ Hallticket {hallticket} not found.")
        return return_response({'status': 'not_found'})
