# Cloudflare DDNS Updater

Este projeto é um script Python para atualizar automaticamente um registro DNS do tipo A na Cloudflare com o IP público atual da máquina. Ele é útil para configurar um DNS dinâmico (DDNS) em domínios gerenciados pela Cloudflare.

## Como funciona

1. Obtém o IP público atual da máquina usando serviços como `api.ipify.org` ou `ifconfig.me`.
2. Consulta a API da Cloudflare para obter o ID da zona e do registro DNS.
3. Compara o IP público atual com o IP registrado no DNS.
4. Atualiza o registro DNS caso o IP tenha mudado.

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```env
   CLOUDFLARE_API_TOKEN=seu_token_da_cloudflare
   ZONE_NAME=seu_nome_da_zona
   RECORD_NAME=seu_nome_do_registro
   ```
2. Certifique-se de que o token da API tenha permissões para ler e atualizar registros DNS.

## Dependências

Instale as dependências do projeto com:
```bash
pip install -r requirements.txt
```

## Uso

Execute o script com:
```bash
python cloudflare_ddns.py
```

## Observação

Certifique-se de configurar corretamente as variáveis no arquivo `.env` para corresponderem ao seu domínio e subdomínio.