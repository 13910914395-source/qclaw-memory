#!/usr/bin/env python3
"""
钉钉 API - 获取审批模板列表
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
print("钉钉 API 测试 - 获取审批模板列表")
print("=" * 50)

# 1. 获取 token
token_resp = get(f"https://oapi.dingtalk.com/gettoken?appkey={APP_KEY}&appsecret={APP_SECRET}")
token = token_resp.get("access_token")
print(f"✅ Token: {token[:20]}...")

# 2. 获取审批模板列表
print("\n[2] 获取审批模板列表...")
process_resp = post(f"https://oapi.dingtalk.com/topapi/process/list?access_token={token}", {
    "offset": 0,
    "size": 50
})
print(f"结果: {json.dumps(process_resp, ensure_ascii=False)[:1000]}")

# 3. 如果有模板，尝试用第一个 process_code 获取审批实例
if process_resp.get("errcode") == 0:
    processes = process_resp.get("result", {}).get("list", [])
    if processes:
        first_process = processes[0]
        print(f"\n[3] 尝试用第一个模板 '{first_process.get('name', '未知')}' (code: {first_process.get('process_code', '无')}) 获取审批实例...")
        
        start = int((time.time() - 30*24*3600) * 1000)
        end = int(time.time() * 1000)
        
        instance_resp = post(f"https://oapi.dingtalk.com/topapi/processinstance/list?access_token={token}", {
            "process_code": first_process.get('process_code', ''),
            "start_time": start,
            "end_time": end,
            "size": 10,
            "cursor": 0
        })
        print(f"结果: {json.dumps(instance_resp, ensure_ascii=False)[:1000]}")
    else:
        print("⚠️ 未找到审批模板")
else:
    print("⚠️ 获取审批模板失败")

print("\n" + "=" * 50)