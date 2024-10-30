# Hanafuda
Automate grow for Hana Network Hanafuda campaign

# Registration
register on https://hanafuda.hana.network/ using google account

use code 
```
W313YG
```
Deposit minimum 1wei (0.000000000000000001 ETH) on ARB/Base chain

Deposit more to obtain more grow attempt every hour

DON'T DEPOSIT DIRECTLY TO SC, MUST USE THE UI ON HANAFUDA

# Installation
Install python and pip
```
sudo apt update && sudo apt install -y python3 python3-pip && python3 --version && pip3 --version
```
Git clone
```
git clone https://github.com/frostnova0x/Hanafuda.git
cd Hanafuda
```
Install dependencies
```
pip install -r requirements.txt
```
get API and Refresh token from inspect element

![image](https://github.com/user-attachments/assets/417911e0-dc0a-4b97-bc62-e74133905332)
create .env (nano .env) and fill with :
```
API_KEY=your_api_key_here (start with AIxxxxxxxxxx)
REFRESH_TOKEN=your_refresh_token_here (start with AMf-xxxx)
# PROXY_URL=optional_proxy_url_here #optional
```
Run script
```
python3 hanagrow.py
```
Set grow amount and enjoy
