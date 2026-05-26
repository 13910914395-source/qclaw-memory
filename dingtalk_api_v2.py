#!/usr/bin/env python3
"""
钉钉 API 测试脚本 - 审批与群聊数据
使用不同的 API 端点
"""
import json
import urllib.request
import urllib.parse
import ssl
import time

# ============== 配置 ==============
APP_KEY = "dingcw44lm5wneb5qlzh"
APP_SECRET = "behUBv34u1lndQPyHIVsQSx6-Zc00yN3_p8ozRtejOpuIE0d6C-YAMXpEvr6Se7v"

# ============== 工具函数 ==============
def create_ssl_context():
    """创建 SSL 上下文，忽略证书验证"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def http_get(url, params=None):
    """GET 请求"""
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    ctx = create_ssl_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}

def http_post(url, data=None):
    """POST 请求"""
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8") if data else None)
    req.add_header("Content-Type", "application/json")
    ctx = create_ssl_context()
    try:
        with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        return {"errcode": -1, "errmsg": str(e)}

# ============== API 函数 ==============
def get_access_token():
    """获取 access_token"""
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    result = http_get(url, params)
    if result.get("access_token"):
        return result["access_token"]
    else:
        print(f"❌ 获取 access_token 失败: {result}")
        return None

def get_approval_list_v2(token):
    """获取审批实例列表 - V2 接口"""
    url = "https://oapi.dingtalk.com/topapi/v2/processinstance/list"
    data = {
        "process_code": "",  # 不指定流程类型，获取所有
        "start_time": int((time.time() - 7*24*3600) * 1000),  # 最近7天
        "end_time": int(time.time() * 1000),
        "size": 10,
        "cursor": 0
    }
    result = http_post(url, data)
    return result

def get_approval_list_by_code(token, process_code):
    """根据流程模板获取审批实例"""
    url = "https://oapi.dingtalk.com/topapi/processinstance/listid"
    data = {
        "process_code": process_code,
        "start_time": int((time.time() - 7*24*3600) * 1000),
        "end_time": int(time.time() * 1000),
        "cursor": 0,
        "size": 20
    }
    result = http_post(url, data)
    return result

def get_chat_list(token):
    """获取群列表 - OAPI 接口"""
    url = "https://oapi.dingtalk.com/topapi/chat/list"
    data = {
        "offset": 0,
        "size": 20
    }
    result = http_post(url, data)
    return result

def get_chat_messages(token, chat_id, start_time=None):
    """获取群消息"""
    url = "https://oapi.dingtalk.com/topapi/chat/listmessages"
    if start_time is None:
        start_time = int((time.time() - 7*24*3600) * 1000)
    data = {
        "chatid": chat_id,
        "start_time": start_time,
        "size": 20
    }
    result = http_post(url, data)
    return result

# ============== 主程序 ==============
if __name__ == "__main__":
    print("=" * 60)
    print("钉钉 API 测试 - 审批与群聊数据")
    print("=" * 60)

    # 1. 获取 access_token
    print("\n[1] 获取 access_token...")
    token = get_access_token()
    if not token:
        print("❌ 无法获取 access_token，退出")
        exit(1)
    print(f"✅ 获取成功: {token[:20]}...")

    # 2. 尝试获取审批列表 - V2 接口
    print("\n[2] 获取审批实例列表（V2接口）...")
    result = get_approval_list_v2(token)
    if result.get("errcode") == 0:
        print(f"✅ 成功! 共 {len(result.get('result', {}).get('list', []))} 条审批")
        for item in result.get("result", {}).get("list", [])[:3]:
            print(f"   - {item.get('title', '无标题')} | {item.get('status', '')}")
    else:
        print(f"❌ 失败: {result.get('errmsg', result)}")

    # 3. 尝试获取群列表
    print("\n[3] 获取群列表...")
    chat_result = get_chat_list(token)
    if chat_result.get("errcode") == 0:
        chat_list = chat_result.get("result", {}).get("chat_id_list", [])
        print(f"✅ 成功! 找到 {len(chat_list)} 个群")
        
        # 尝试获取第一个群的消息
        if chat_list:
            print(f"\n[4] 尝试获取群 {chat_list[0]} 的消息...")
            msg_result = get_chat_messages(token, chat_list[0])
            if msg_result.get("errcode") == 0:
                msgs = msg_result.get("result", {}).get("list", [])
                print(f"✅ 成功! 最近 {len(msgs)} 条消息")
                for m in msgs[:3]:
                    print(f"   - {m.get('sender', '未知')}: {m.get('msgtype', '')}")
            else:
                print(f"❌ 获取消息失败: {msg_result.get('errmsg', msg_result)}")
    else:
        print(f"❌ 失败: {chat_result.get('errmsg', chat_result)}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)