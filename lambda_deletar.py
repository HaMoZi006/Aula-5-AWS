import boto3
import json
import os

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('musicas')
s3       = boto3.client('s3')
BUCKET   = os.environ.get('BUCKET_NAME')


def lambda_handler(event, context):
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body or '{}')

    musica_id = body.get('id', '').strip()
    s3_key    = body.get('s3Key', '').strip()
    thumb_key = body.get('thumbKey', '').strip()

    if not musica_id:
        return resposta(400, {'error': 'Campo "id" é obrigatório'})

    # ── Deleta os arquivos do S3 ──────────────────────────────────────────────
    if s3_key:
        s3.delete_object(Bucket=BUCKET, Key=s3_key)
        print(f"S3 deletado: {s3_key}")

    if thumb_key:
        s3.delete_object(Bucket=BUCKET, Key=thumb_key)
        print(f"S3 capa deletada: {thumb_key}")

    # ── Deleta o item do DynamoDB ─────────────────────────────────────────────
    table.delete_item(Key={'id': musica_id})
    print(f"DeleteItem: id={musica_id}")

    return resposta(200, {'ok': True})


def resposta(status, body):
    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body),
    }