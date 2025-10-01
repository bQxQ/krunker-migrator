import requests,time

API="http://127.0.0.1:5000"

class C:
 def __init__(s,u=API):s.u=u
 def h(s):
  try:r=requests.get(s.u+"/health",timeout=5);return r.ok
  except:return 0
 def g(s):
  try:
   r=requests.post(s.u+"/get-email-only",timeout=10)
   if r.ok:d=r.json();return d.get("email"),d.get("session_id")
  except Exception as e:print("err g",e)
  return None,None
 def w(s,i,t=60):
  try:
   r=requests.post(s.u+"/get-code-for-session",json={"session_id":i,"timeout":t},timeout=t+5)
   if r.ok:d=r.json();return d.get("verification_code")
  except Exception as e:print("err w",e)
  return None

if __name__=="__main__":
 c=C()
 print("[*] check api...")
 if not c.h():print("[!] api dead");exit()
 print("[+] api online")
 print("[*] gen mail...")
 e,i=c.g()
 if not e:print("[!] fail mail");exit()
 print(f"[+] generated {e} ({i})")
 print("[*] wait code..")
 k=c.w(i,60)
 if k:print(f"[+] code {k}")
 else:print("[!] no code")
