#!/usr/bin/env python3
"""
钉钉 API 测试脚本 - 修正版
"""
import json
import urllib.request
import urllib.parse
import ssl
import time

# 配置
APP_KEY = "dingcw44lm5wneb5qlzh"
APP_SECRET = "behUBv34u1lndQPyHIVsQSx6-Zc00yN3_p8ozRtejOpuIE0d6C-YAMXpEvr6Se7v"

def ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def get(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as response:
        return json.loads(response.read().decode())

def post(url, data):
    req = urllib.request.Request(url, data=json.dumps(data).encode())
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=30, context=ssl_context()) as response:
        return json.loads(response.read().decode())

# 1. 获取 token
print("=" * 50)
print("钉钉 API 测试")
print("=" * 50)
print("\n[1] 获取 access_token...")
token_resp = get("https://oapi.dingtalk.com/gettoken", {
    "appkey": APP_KEY,
    "appsecret": APP_SECRET
})
token = token_resp.get("access_token")
print(f"✅ Token: {token[:20]}..." if token else f"❌ 失败: {token_resp}")

if not token:
    exit(1)

# 2. 尝试用旧的 listid 接口
print("\n[2] 获取审批列表 (processinstance/listid)...")
approval_resp = post("https://oapi.dingtalk.com/topapi/processinstance/listid", {
    "process_code": "",
    "start_time": int((time.time() - 7*24*3600)*1000),
    "end_time": int(time.time()*1000),
    "cursor": 0,
    "size": 10
})
print(f"结果: {json.dumps(approval_resp, ensure_ascii=False)[:500]}")

# 3. 获取群列表
print("\n[3] 获取群列表 (chat/list)...")
chat_resp = get("https://oapi.dingtalk.com/chat/list", {"access_token": token})
print(f"结果: {json.dumps(chat_resp, ensure_ascii=False)[:500]}")

# 4. 用 topapi 获取群列表
print("\n[4] 获取群列表 (topapi/chat/list)...")
chat_resp2 = post("https://oapi.dingtalk.com/topapi/chat/list", {
    "offset": 0,
    "size": 20
})
print(f"结果: {json.dumps(chat_resp2, ensure_ascii=False)[:500]}")

print("\n" + "=" * 50)
print("完成")
print("=" * 50)