import requests, json, time, re;from flask import Flask,request,jsonify
class Z: G,Y,C,E,W="\033[92m","\033[93m","\033[96m","\033[91m","\033[0m"
li=lambda m:print(f"{Z.C}[INFO]{Z.W} {m}");ls=lambda m:print(f"{Z.G}[SUCCESS]{Z.W} {m}");lw=lambda m:print(f"{Z.Y}[WARN]{Z.W} {m}");le=lambda m:print(f"{Z.E}[ERROR]{Z.W} {m}")
app=Flask(__name__)
API,NEW,LOOK="/emails/new-email","/emails/new-email","/emails/emails";INT,TO,FILTER=3,180,"noreply@frvr.com"
CODES=[r'<(?:td|p|div|span)[^>]*>\s*(\d{6})\s*</(?:td|p|div|span)>',r'>(\d{6})<',r'(\d{6})',r'(?:code|verification|otp)[^0-9]*(\d{6})',r'(\d{6})[^0-9]*(?:code|verification|complete)',r'(?:registration|account|verify)[^0-9]*(\d{6})',r'\b(?:your|the)\s+(?:code|verification|otp)(?:\s+(?:is|:))?\s*(\d{6})\b',r'[^a-zA-Z](\d{6})[^a-zA-Z]']
EXC=[r'#[0-9a-fA-F]{6}',r'color:\s*[#]?(\d{6})',r'rgba?\([^)]*(\d{6})',r'font-size:\s*(\d{6})',r'width:\s*(\d{6})',r'height:\s*(\d{6})',r'margin:\s*(\d{6})',r'padding:\s*(\d{6})']

def grab(txt):
 if not txt:return None
 for p in EXC: txt=re.sub(p,'[REMOVED]',txt,flags=re.I)
 for i,p in enumerate(CODES):
  try:
   m=re.findall(p,txt,re.I|re.S); 
   if m:
    for c in m:
     c=str(c).strip()
     if len(c)==6 and c.isdigit() and not c.startswith(('19','20','000')) and c not in ['123456','000000','111111','222222','333333','444444','555555','666666','777777','888888','999999'] and len(set(c))>1:return c
  except: continue
 nums=re.findall(r'\b(\d{6})\b',txt)
 for n in nums:
  if not n.startswith(('19','20','000')) and n not in ['123456','000000','111111','222222','333333','444444','555555','666666','777777','888888','999999'] and len(set(n))>1:return n

class E:                                      # add ur proxies here if u dont want ratelimit (u can do proxyless)
 def __init__(s): s.s=requests.Session();px="# PROXY HERE";s.s.proxies.update({"http":f"http://{px}","https":f"http://{px}"});li(f"Proxy {px}")
 def new(s):
  try:
   r=s.s.post("https://mail-api.pineapple-berry.pro"+NEW,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json","Content-Type":"application/json"},timeout=15);r.raise_for_status();d=r.json();em,tk=d.get("email"),d.get("authKey")
   if not em or not tk: raise RuntimeError("Missing email/token")
   return em,tk
  except Exception as e: le(f"fail new: {e}");return None,None
 def poll(s,em,tk,t=30):
  url="https://mail-api.pineapple-berry.pro"+LOOK;h={"User-Agent":"Mozilla/5.0","Accept":"application/json","authorization":tk};dl=time.time()+t
  while time.time()<dl:
   try:r=s.s.get(url,headers=h,params={"emailAddress":em},timeout=15)
   except Exception as e: time.sleep(INT);continue
   if r.status_code==403:return None
   if r.status_code==304:time.sleep(INT);continue
   if r.status_code!=200:time.sleep(INT);continue
   try:msgs=r.json()
   except:time.sleep(INT);continue
   if not isinstance(msgs,list):time.sleep(INT);continue
   for m in msgs:
    f=(m.get("from")or"").lower();sb=m.get("subject")or"";b=m.get("textBody")or m.get("preview")or m.get("html")or""
    if FILTER in f or FILTER in sb.lower() or 'verification' in f or 'noreply' in f or 'krunker' in f:
     c=grab(b); 
     if c:return c
   time.sleep(INT)
  return None

S={}

@app.route('/health') 
def h(): return jsonify({'status':'ok'})
@app.route('/get-email-only',methods=['POST'])
def g1():
 g=E();em,tk=g.new(); 
 if not em or not tk: return jsonify({'error':'fail'}),500
 sid=str(hash(em+str(time.time())));S[sid]={'email':em,'token':tk,'generator':g,'status':'ready'}
 return jsonify({'success':True,'email':em,'session_id':sid})
@app.route('/get-code-for-session',methods=['POST'])
def g2():
 d=request.json;sid=d.get('session_id');t=d.get('timeout',30)
 if sid not in S:return jsonify({'error':'bad id'}),400
 s=S[sid];c=s['generator'].poll(s['email'],s['token'],t)
 if c: s['status']='found';return jsonify({'success':True,'email':s["email"],'verification_code':c})
 s['status']='timeout';return jsonify({'error':'timeout'}),408
@app.route('/status/<sid>')
def g3(sid): return jsonify({'email':S.get(sid,{}).get('email','?'),'status':S.get(sid,{}).get('status','?')})

if __name__=="__main__":app.run(host='0.0.0.0',port=5000)
