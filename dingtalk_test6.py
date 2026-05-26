#!/usr/bin/env python3
"""
钉钉 API - 修正参数与路径
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

def get(url):
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
token = get(f"https://oapi.dingtalk.com/gettoken?appkey={APP_KEY}&appsecret={APP_SECRET}")["access_token"]
print(f"✅ Token: {token[:20]}...")

# 2. 获取审批列表 - 正确参数
print("\n[2] 获取审批列表...")
start = int((time.time() - 30*24*3600) * 1000)  # 最近30天
end = int(time.time() * 1000)
resp = post(f"https://oapi.dingtalk.com/topapi/processinstance/list?access_token={token}", {
    "start_time": start,
    "end_time": end,
    "size": 10,
    "cursor": 0
})
print(f"结果: {json.dumps(resp, ensure_ascii=False)[:800]}")

# 3. 获取群列表 - 用 topapi
print("\n[3] 获取群列表...")
chat_resp = post(f"https://oapi.dingtalk.com/topapi/chat/list?access_token={token}", {
    "offset": 0,
    "size": 20
})
print(f"结果: {json.dumps(chat_resp, ensure_ascii=False)[:500]}")

# 4. 尝试获取用户所在群
print("\n[4] 获取用户所在群...")
user_resp = get(f"https://oapi.dingtalk.com/user/list?access_token={token}&offset=0&size=10")
print(f"结果: {json.dumps(user_resp, ensure_ascii=False)[:500]}")

print("\n" + "=" * 50)