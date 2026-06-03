import boto3
import json

dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('musicas')


def lambda_handler(event, context):
    # Scan retorna todos os itens da tabela
    resultado = table.scan()
    musicas   = resultado.get('Items', [])

    # Ordena por nome já que DynamoDB não garante ordem
    musicas.sort(key=lambda m: m.get('nome', ''))

    print(f"Scan: {len(musicas)} músicas retornadas")
    return resposta(200, musicas)


def resposta(status, body):
    return {
        'statusCode': status,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body),
    }