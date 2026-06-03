import boto3
import json
import os
import uuid

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('musicas')


def lambda_handler(event, context):
    body = event.get('body', '{}')
    if isinstance(body, str):
        body = json.loads(body or '{}')

    nome      = body.get('nome', '').strip()
    url       = body.get('url', '').strip()
    thumb     = body.get('thumb', None)
    s3_key    = body.get('s3Key', None)
    thumb_key = body.get('thumbKey', None)

    if not nome or not url:
        return resposta(400, {'error': 'Campos "nome" e "url" são obrigatórios'})

    # Gera um id único pra ser a partition key do item
    novo_id = str(uuid.uuid4())

    item = {
        'id':   novo_id,
        'nome': nome,
        'url':  url,
    }
    if thumb:     item['thumb']     = thumb
    if s3_key:    item['s3_key']    = s3_key
    if thumb_key: item['thumb_key'] = thumb_key

    # PutItem é atômico — sem risco de conflito com uploads simultâneos
    table.put_item(Item=item)
    print(f"PutItem: id={novo_id} nome='{nome}'")

    return resposta(200, {'ok': True, 'id': novo_id})


def resposta(status, body):
    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body),
    }