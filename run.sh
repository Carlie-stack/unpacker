#!/bin/bash

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo -e "${CYAN}LUARMOR UNPACKER CLI${NC}"

if [ "$#" -ne 1 ]; then
    echo -e "${RED}[!] Error: Invalid number of arguments.${NC}"
    echo -e "${YELLOW}[*] Usage: ./run.sh <LOADER_URL>${NC}"
    echo -e "${YELLOW}[*] Example: ./run.sh https://api.luarmor.net/files/v4/loaders/xxxx.lua${NC}"
    exit 1
fi

TARGET_URL="$1"
echo -e "${BLUE}[*] Target:${NC} $TARGET_URL"

if [[ ! "$TARGET_URL" =~ ^https?:// ]]; then
    echo -e "${RED}[!] Error: URL must start with http:// or https://${NC}"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR" || exit 1

mkdir -p output

export TARGET_URL

python3 -c "
import os
import sys
import logging
from extractor import fetch_url, extract_all_lua_urls, save_to_file

logging.basicConfig(level=logging.ERROR)

url = os.environ.get('TARGET_URL')

print('\n\033[0;34m[>] Fetching Loader...\033[0m')
try:
    code = fetch_url(url)
    save_to_file(code, 'output/loader.lua')
    print(f'    \033[0;32m[+]\033[0m Received {len(code)} bytes.')
    print(f'    \033[0;32m[+]\033[0m Saved to output/loader.lua')
except Exception as e:
    print(f'    \033[0;31m[!]\033[0m Error: {e}')
    sys.exit(1)

print('\n\033[0;34m[>] Extracting CDN URLs...\033[0m')
urls = extract_all_lua_urls(code)

if not urls:
    print('    \033[1;33m[-]\033[0m No valid CDN URLs found.')
    sys.exit(2)

cdn_url = urls[0]
print(f'    \033[0;32m[+]\033[0m Endpoint found: {cdn_url}')

print('\n\033[0;34m[>] Fetching CDN Script...\033[0m')
try:
    cdn_code = fetch_url(cdn_url)
    save_to_file(cdn_code, 'output/cdn_script.lua')
    print(f'    \033[0;32m[+]\033[0m Received {len(cdn_code)} bytes.')
    print(f'    \033[0;32m[+]\033[0m Saved to output/cdn_script.lua')
except Exception as e:
    print(f'    \033[0;31m[!]\033[0m Error: {e}')
    sys.exit(1)

print('\n\033[0;32m[✓] Process completed successfully.\033[0m')
"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "\n${GREEN}[✓] Done. Check the 'output/' directory.${NC}"
elif [ $EXIT_CODE -eq 2 ]; then
    echo -e "\n${YELLOW}[-] Finished, but no CDN script was found.${NC}"
else
    echo -e "\n${RED}[!] Process failed with exit code $EXIT_CODE.${NC}"
fi
