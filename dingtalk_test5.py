#!/usr/bin/env python3
"""
钉钉 API - 修正 API 名称
"""
import json
import urllib.request
import urllib.parse
import ssl
import time

APP_KEY = "dingcw44lm5wneb5qlzh"
APP_SECRET = "behUBv34u1lndQPyHIVsQSx6-Zc00yN3_p8ozRtejOpuIE0d6C-YAMXpEvr6Se7v"

def ssl_ctx():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=30, context=ssl_ctx()) as resp:
        return json.loads(resp.read().decode())

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode())
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30, context=ssl_ctx()) as resp:
        return json.loads(resp.read().decode())

print("=" * 50)
print("钉钉 API 测试")
print("=" * 50)

# 1. 获取 token
print("\n[1] 获取 access_token...")
token_resp = get("https://oapi.dingtalk.com/gettoken", {
    "appkey": APP_KEY,
    "appsecret": APP_SECRET
})
token = token_resp.get("access_token")
print(f"✅ Token: {token[:20]}...")

# 2. 正确的审批API - topapi/processinstance/list
print("\n[2] 获取审批列表 (topapi/processinstance/list)...")
start_time = int((time.time() - 7*24*3600) * 1000)
end_time = int(time.time() * 1000)
approval_resp = post(f"https://oapi.dingtalk.com/topapi/processinstance/list?access_token={token}", {
    "process_code": "",
    "start_time": start_time,
    "end_time": end_time,
    "cursor": 0,
    "size": 20
})
print(f"结果: {json.dumps(approval_resp, ensure_ascii=False)}")

# 3. 正确的群列表API - chat/list
print("\n[3] 获取群列表 (chat/list)...")
chat_resp = get(f"https://oapi.dingtalk.com/chat/list?access_token={token}")
print(f"结果: {json.dumps(chat_resp, ensure_ascii=False)}")

print("\n" + "=" * 50)