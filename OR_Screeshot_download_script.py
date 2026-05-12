#1. Open Command Prompt or Terminal.
#2. Navigate to the directory where you want to save the script using the cd command.
#3. create a new Python file using a text editor or by running the command: touch OR_Screeshot_download_script.py
#4. Copy and paste the following code into the OR_Screeshot_download_script.py
#5. Save the file.
#6. Run set NODE_TLS_REJECT_UNAUTHORIZED=0 in Command Prompt to bypass SSL issues if needed.
#7. Run pip install requests to install the requests library if you haven't already.
#8. Finally, execute the script by running: python OR_Screeshot_download_script.py
# This script will download all screenshots from the receipts in your Supabase database and save them in a folder named 'vsd_screenshots'. 
# Make sure to replace the SUPABASE_URL and SUPABASE_KEY with your actual Supabase project details.

import requests, os, csv

# Your Supabase details
SUPABASE_URL = 'https://kofalhqgjuglfjcinwdh.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtvZmFsaHFnanVnbGZqY2lud2RoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc1NDI2NzYsImV4cCI6MjA5MzExODY3Nn0.JDV29I2PL-Ps3r5ahgC7p9-lNhMztaVpf6N1c4oQ0c8'
DOWNLOAD_FOLDER = 'vsd_screenshots'

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Fetch all receipts with screenshot URLs
response = requests.get(
    f'{SUPABASE_URL}/rest/v1/receipts?select=receipt_id,screenshot_url&screenshot_url=not.is.null',
    headers={
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}'
    }
)

records = response.json()
print(f"Found {len(records)} screenshots")

for r in records:
    url = r['screenshot_url']
    receipt_id = r['receipt_id']
    if not url: continue
    try:
        img = requests.get(url)
        ext = url.split('.')[-1].split('?')[0] or 'jpg'
        filename = f"{DOWNLOAD_FOLDER}/{receipt_id}.{ext}"
        with open(filename, 'wb') as f:
            f.write(img.content)
        print(f"✅ Downloaded: {receipt_id}")
    except Exception as e:
        print(f"❌ Failed {receipt_id}: {e}")

print(f"\nDone! Files saved in '{DOWNLOAD_FOLDER}' folder")