#!/bin/bash

# Define a URL e o intervalo de verificação (em segundos)
URL="http://localhost:5000/health_check"
INTERVAL=300  # 5 minutos

while true; do
    # Faz a requisição e obtém o código de status HTTP
    HTTP_CODE=$(curl --write-out "%{http_code}" --silent --output /dev/null "$URL")

    # Verifica se o código de status é diferente de 200
    if [ "$HTTP_CODE" -ne 200 ]; then
        echo "$(date): Serviço não está respondendo com 200. Reiniciando..."

        # Reinicia o serviço. Substitua 'whatsapp_api.service' pelo nome do serviço correto
        sudo systemctl restart whatsapp_api.service

        echo "$(date): Serviço reiniciado."
    else
        echo "$(date): Serviço funcionando normalmente (HTTP 200)."
    fi

    # Aguarda o próximo intervalo antes de verificar novamente
    sleep "$INTERVAL"
done

