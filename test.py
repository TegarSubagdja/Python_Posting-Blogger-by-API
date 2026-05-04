import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests

response = requests.get("https://pure.md/https://suryasarana.com/brands/thk")

print(response.text)