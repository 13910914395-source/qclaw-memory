#!/usr/bin/env python3
"""
钉钉 API - 尝试其他常见端点
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
print("钉钉 API 测试 - 尝试其他端点")
print("=" * 50)

# 1. 获取 token
token_resp = get(f"https://oapi.dingtalk.com/gettoken?appkey={APP_KEY}&appsecret={APP_SECRET}")
token = token_resp.get("access_token")
print(f"✅ Token: {token[:20]}...")

# 2. 尝试获取用户信息
print("\n[2] 尝试获取用户信息...")
user_resp = get(f"https://oapi.dingtalk.com/user/getuserinfo?access_token={token}&code=xxx")
print(f"结果: {json.dumps(user_resp, ensure_ascii=False)[:500]}")

# 3. 尝试获取部门列表
print("\n[3] 尝试获取部门列表...")
dept_resp = get(f"https://oapi.dingtalk.com/department/list?access_token={token}")
print(f"结果: {json.dumps(dept_resp, ensure_ascii=False)[:500]}")

# 4. 尝试获取应用信息
print("\n[4] 尝试获取应用信息...")
app_resp = get(f"https://oapi.dingtalk.com/topapi/app/get?access_token={token}")
print(f"结果: {json.dumps(app_resp, ensure_ascii=False)[:500]}")

print("\n" + "=" * 50)