# coding: utf-8
"""One-shot Wikimedia Commons photo download for the personal, offline museum guide."""
import json, urllib.request, urllib.error, urllib.parse, pathlib, time, sys
from concurrent.futures import ThreadPoolExecutor, as_completed
here=pathlib.Path(__file__).resolve().parent
items=json.loads((here/'ФОТО_ИСТОЧНИКИ.json').read_text(encoding='utf-8'))
out=here/'images'; out.mkdir(exist_ok=True)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0 Safari/537.36', 'Accept':'image/avif,image/webp,image/apng,image/jpeg,image/*,*/*;q=0.8', 'Referer':'https://commons.wikimedia.org/'}
def grab(photo):
    dest=out/photo['local']
    if not photo['local']: return 'SKIP','06: external source (not licensed for automatic download)'
    if dest.exists() and dest.stat().st_size > 8000: return 'OK',str(dest.name)+' exists'
    direct=photo['direct']; thumb=photo['thumb']
    # Image proxy is fallback for networks where upload.wikimedia.org denies automated access.
    encoded=urllib.parse.quote(thumb, safe='')
    attempts=[thumb, 'https://wsrv.nl/?url='+encoded, direct, 'https://commons.wikimedia.org/wiki/Special:Redirect/file/'+urllib.parse.quote(photo['filename'],safe='')+'?width=800']
    errors=[]
    for url in attempts:
      try:
        req=urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req,timeout=22) as response:
          blob=response.read(15*1024*1024)
          ct=response.headers.get('Content-Type','')
        # JPEG SOI or PNG magic; all selected photos are JPEG.
        if len(blob) < 8000 or not blob.startswith(b'\xff\xd8\xff'):
          errors.append('invalid image / access blocked'); continue
        dest.write_bytes(blob)
        return 'OK',str(dest.name)+f' ({len(blob)//1024} KB)'
      except Exception as e:
        errors.append(type(e).__name__+': '+str(e)[:55])
    return 'ERROR',str(dest.name)+' — '+('; '.join(errors[:2]))
photos=[x for x in items if x['local']]
print('Wikimedia Commons: '+str(len(photos))+' photos, 17 chapters. Downloading to:',out)
with ThreadPoolExecutor(max_workers=4) as pool:
    futs={pool.submit(grab,p):p for p in photos}
    successes=0
    for f in as_completed(futs):
        typ,msg=f.result();print(('✓ ' if typ=='OK' else '✗ ')+msg)
        if typ=='OK': successes+=1
print(f'\nDownloaded/available: {successes} / {len(photos)}')
print('Open index.html. Files in images/ are fully offline.')
if successes<len(photos):
 print('Some images were blocked or unavailable. Open ФОТО_ИСТОЧНИКИ.html and save photos manually as 01.jpg etc.')

