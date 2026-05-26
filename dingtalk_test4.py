#!/usr/bin/env python3
"""
钉钉 API - 尝试获取应用当前权限列表
"""
import json
import urllib.request
import urllib.parse
import ssl

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

print("获取 access_token...")
token_resp = get("https://oapi.dingtalk.com/gettoken", {
    "appkey": APP_KEY,
    "appsecret": APP_SECRET
})
token = token_resp.get("access_token")
print(f"Token: {token[:20]}...")

# 尝试获取企业授权码（OAuth）
print("\n尝试获取企业授权码...")
oauth_resp = post("https://oapi.dingtalk.com/sso/gettoken", {
    "corpid": "dinge80c9c03a744c34135c2f4657eb6378f",  # 你的企业ID
    "corpsecret": APP_SECRET  # 应用Secret
})
print(f"结果: {json.dumps(oauth_resp, ensure_ascii=False)[:300]}")

# 尝试不同格式的审批API
print("\n尝试审批API - v2格式...")
resp1 = post("https://oapi.dingtalk.com/topapi/v2/processinstance/list", {
    "process_code": "",
    "start_time": 0,
    "end_time": int(1000*3600*24*7),
    "size": 10,
    "cursor": 0
})
print(f"结果: {json.dumps(resp1, ensure_ascii=False)[:300]}")

# 尝试获取corp token
print("\n获取 Corp Token...")
corp_resp = get("https://oapi.dingtalk.com/gettoken", {
    "appkey": "dinge80c9c03a744c34135c2f4657eb6378f",  # 企业ID作为appkey
    "appsecret": APP_SECRET
})
print(f"结果: {json.dumps(corp_resp, ensure_ascii=False)[:300]}")