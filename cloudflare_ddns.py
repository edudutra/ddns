import os
import requests
from dotenv import load_dotenv
import datetime
import logging

# Carrega variáveis do arquivo .env
load_dotenv()

# CONFIGURAÇÕES
ZONE_NAME = os.getenv("CLOUDFLARE_ZONE_NAME")
RECORD_NAME = os.getenv("CLOUDFLARE_RECORD_NAME")
API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")

if not API_TOKEN:
    raise Exception("API Token não encontrado! Verifique o arquivo .env")
if not ZONE_NAME or not RECORD_NAME:
    raise Exception("ZONE_NAME ou RECORD_NAME não encontrados! Verifique o arquivo .env")

# Cabeçalhos padrão da API
headers = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler("logs/logs.txt", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)

# Função para pegar o IP público com a opção verify=False
def get_public_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text.strip()
    except requests.exceptions.RequestException:
        logger.error("Erro ao obter o IP público com api.ipify.org. Tentando alternativa...")
        return requests.get("https://ifconfig.me/ip", timeout=5).text.strip()

def get_zone_id():
    url = f"https://api.cloudflare.com/client/v4/zones"
    params = {"name": ZONE_NAME}
    resp = requests.get(url, headers=headers, params=params)
    return resp.json()["result"][0]["id"]

def get_record_id(zone_id):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    params = {"type": "A", "name": RECORD_NAME}
    resp = requests.get(url, headers=headers, params=params)
    result = resp.json()["result"]
    if not result:
        raise Exception(f"Registro A '{RECORD_NAME}' não encontrado na zona '{ZONE_NAME}'")
    return result[0]["id"], result[0]["content"]

def update_dns_record(zone_id, record_id, ip):
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    data = {
        "type": "A",
        "name": RECORD_NAME,
        "content": ip,
        "ttl": 300,  # 5 minutos
        "proxied": False  # Não usar proxy (para SSH, etc.)
    }
    resp = requests.put(url, headers=headers, json=data)
    return resp.json()["success"]

def main():
    ip = get_public_ip()
    logger.info(f"IP atual: {ip}")

    zone_id = get_zone_id()
    record_id, current_ip = get_record_id(zone_id)

    if ip != current_ip:
        logger.info(f"IP mudou (antes: {current_ip}) — atualizando...")
        success = update_dns_record(zone_id, record_id, ip)
        if success:
            logger.info("Registro atualizado com sucesso!")
        else:
            logger.error("Falha ao atualizar o registro.")
    else:
        logger.info("IP não mudou. Nada a fazer.")

if __name__ == "__main__":
    main()
