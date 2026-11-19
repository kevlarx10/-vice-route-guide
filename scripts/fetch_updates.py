#!/usr/bin/env python3
"""Build spoiler-hidden news index from trusted RSS feeds; uses Python standard library."""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
from urllib.request import Request,urlopen
from urllib.parse import urlparse, quote
from xml.etree import ElementTree as ET
from pathlib import Path
import hashlib,json,re,sys,time

OUT=Path(__file__).resolve().parents[1]/'site'/'updates.json'
DEFAULT=json.loads(OUT.read_text()) if OUT.exists() else {'items':[]}
SOURCES=[
 ('PowerPyx','guide','https://www.powerpyx.com/feed/'),
 ('VGC','guide','https://www.videogameschronicle.com/feed/'),
 ('PC Gamer','guide','https://www.pcgamer.com/feeds/all/'),
 ('Rockstar Games','official','https://news.google.com/rss/search?q='+quote('"Grand Theft Auto VI" site:rockstargames.com/newswire when:30d')+'&hl=en-US&gl=US&ceid=US:en'),
]
ALLOWED={'www.powerpyx.com','powerpyx.com','www.videogameschronicle.com','videogameschronicle.com','www.pcgamer.com','pcgamer.com','www.rockstargames.com','rockstargames.com','news.google.com'}
PAT=re.compile(r'\b(?:gta\s*(?:6|vi)|grand\s+theft\s+auto\s*(?:6|vi))\b',re.I)
DROP=re.compile(r'\b(?:gta\s*online|gta\s*5|grand\s+theft\s+auto\s*v\b)\b',re.I)

def txt(el,path):
 v=el.find(path);return unescape(''.join(v.itertext()).strip()) if v is not None else ''

def get_items(name,kind,url):
 req=Request(url,headers={'User-Agent':'ViceRouteGuideFeed/1.0 (+https://github.com); RSS reader','Accept':'application/rss+xml, application/atom+xml, text/xml'})
 with urlopen(req,timeout=17) as r:raw=r.read(3_000_000)
 root=ET.fromstring(raw)
 entries=[]
 for node in (root.findall('./channel/item')+root.findall('{http://www.w3.org/2005/Atom}entry'))[:75]:
  title=re.sub(r'<[^>]*>','',txt(node,'title')).strip()
  desc=txt(node,'description')[:240]
  if not PAT.search(title+' '+desc) or (DROP.search(title) and not PAT.search(title)):continue
  link=txt(node,'link')
  if not link:
   a=node.find('{http://www.w3.org/2005/Atom}link');link=a.attrib.get('href','') if a is not None else ''
  if not link or urlparse(link).scheme!='https' or urlparse(link).hostname not in ALLOWED:continue
  if kind=='official':
   source_name=txt(node,'source').lower()
   if source_name and not ('rockstar' in source_name):continue
  if kind=='official' and urlparse(link).hostname=='news.google.com':
   # GNews link leads to the original publisher; still labeled as a link aggregating official Rockstar news.
   pass
  date=txt(node,'pubDate') or txt(node,'{http://www.w3.org/2005/Atom}updated') or txt(node,'{http://purl.org/dc/elements/1.1/}date')
  try: date=parsedate_to_datetime(date).astimezone(timezone.utc).date().isoformat()
  except: date=date[:10] if len(date)>=10 else datetime.now(timezone.utc).date().isoformat()
  ident=hashlib.sha256(link.encode()).hexdigest()[:14]
  entries.append({'id':ident,'title':title[:160],'label':'New GTA VI announcement' if kind=='official' else 'New GTA VI guide or walkthrough','source':name,'kind':kind,'date':date,'url':link})
 return entries

all_items=[];failed=[]
for name,kind,url in SOURCES:
 try:
  result=get_items(name,kind,url);all_items+=result;print(name,len(result))
 except Exception as ex:
  print('Feed unavailable:',name,str(ex),file=sys.stderr);failed.append(name)
# Keep previous articles when an RSS feed temporarily fails, and always keep stable starter links.
all_items+=DEFAULT.get('items',[])
seen=set(); unique=[]
for it in all_items:
 if not isinstance(it,dict) or not isinstance(it.get('url'),str):continue
 url=it['url']; domain=urlparse(url).hostname
 if urlparse(url).scheme!='https' or domain not in ALLOWED:continue
 if url in seen:continue
 seen.add(url);unique.append(it)
unique.sort(key=lambda x:x.get('date',''),reverse=True)
OUT.write_text(json.dumps({'checked':datetime.now(timezone.utc).isoformat(timespec='seconds'),'items':unique[:60],'sources_unavailable':failed},indent=2,ensure_ascii=False)+'\n')
print('Wrote',len(unique[:60]),'links')
