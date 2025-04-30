# Cloudflare DDNS Updater

This project is a Python script to automatically update an A-type DNS record on Cloudflare with the machine's current public IP. It is useful for setting up dynamic DNS (DDNS) on domains managed by Cloudflare.

## How it works

1. Retrieves the machine's current public IP using services like `api.ipify.org` or `ifconfig.me`.
2. Queries the Cloudflare API to get the zone and DNS record IDs.
3. Compares the current public IP with the IP registered in the DNS.
4. Updates the DNS record if the IP has changed.

## Configuration

1. Create a `.env` file in the project's root directory with the following variables:
   ```env
   CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
   ZONE_NAME=your_zone_name
   RECORD_NAME=your_record_name
   ```
2. Ensure the API token has permissions to read and update DNS records.

## Dependencies

Install the project's dependencies with:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with:
```bash
python cloudflare_ddns.py
```

## Note

Make sure to correctly configure the variables in the `.env` file to match your domain and subdomain.

---

[Leia em Português](readme_pt-br.md)