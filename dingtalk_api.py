#!/usr/bin/env python3
"""
钉钉 API 调用脚本
支持：获取审批列表、审批详情、群聊天记录
"""

import json
import urllib.request
import ssl
from datetime import datetime, timedelta

# 钉钉应用凭证
APP_KEY = "dingcw44lm5wneb5qlzh"
APP_SECRET = "behUBv34u1lndQPyHIVsQSx6-Zc00yN3_p8ozRtejOpuIE0d6C-YAMXpEvr6Se7v"

# 创建 SSL 上下文（禁用证书验证以解决 SSL 问题）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def http_get(url, params=None):
    """发送 GET 请求"""
    if params:
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{url}?{query_string}"
    
    req = urllib.request.Request(url, method='GET')
    req.add_header('Content-Type', 'application/json')
    
    with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
        return json.loads(response.read().decode('utf-8'))

def http_post(url, data):
    """发送 POST 请求"""
    req = urllib.request.Request(url, method='POST')
    req.add_header('Content-Type', 'application/json')
    
    json_data = json.dumps(data).encode('utf-8')
    
    with urllib.request.urlopen(req, data=json_data, timeout=30, context=ssl_context) as response:
        return json.loads(response.read().decode('utf-8'))

def get_access_token():
    """获取钉钉 access_token"""
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": APP_KEY,
        "appsecret": APP_SECRET
    }
    
    result = http_get(url, params)
    if result.get("errcode") == 0:
        return result["access_token"]
    else:
        print(f"获取 token 失败: {result}")
        return None

def get_approval_instances(access_token, process_code=None, start_time=None, end_time=None, size=10):
    """获取审批实例列表"""
    url = "https://oapi.dingtalk.com/topapi/processinstance/listids"
    
    # 默认查询最近 7 天
    if not end_time:
        end_time = int(datetime.now().timestamp() * 1000)
    if not start_time:
        start_time = int((datetime.now() - timedelta(days=7)).timestamp() * 1000)
    
    data = {
        "process_code": process_code,
        "start_time": start_time,
        "end_time": end_time,
        "size": size,
        "cursor": 0
    }
    
    result = http_post(f"{url}?access_token={access_token}", data)
    return result

def get_approval_detail(access_token, process_instance_id):
    """获取审批实例详情"""
    url = "https://oapi.dingtalk.com/topapi/processinstance/get"
    
    data = {
        "process_instance_id": process_instance_id
    }
    
    result = http_post(f"{url}?access_token={access_token}", data)
    return result

def get_chat_groups(access_token):
    """获取群列表（需要管理员权限）"""
    url = "https://oapi.dingtalk.com/chat/list"
    
    params = {
        "access_token": access_token,
        "offset": 0,
        "size": 20
    }
    
    result = http_get(url, params)
    return result

def get_group_messages(access_token, open_conversation_id, cursor=None):
    """获取群聊天记录"""
    url = "https://oapi.dingtalk.com/topapi/im/chat/scenegroup/message/query"
    
    data = {
        "open_conversation_id": open_conversation_id,
        "size": 20
    }
    if cursor:
        data["cursor"] = cursor
    
    result = http_post(f"{url}?access_token={access_token}", data)
    return result

# ==================== 主程序 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("钉钉 API 测试 - 审批与群聊数据")
    print("=" * 60)
    
    # 1. 获取 access_token
    print("\n[1] 获取 access_token...")
    token = get_access_token()
    if not token:
        print("❌ 获取 token 失败，请检查 AppKey 和 AppSecret")
        exit(1)
    print(f"✅ 获取成功: {token[:20]}...")
    
    # 2. 获取审批实例列表
    print("\n[2] 获取审批实例列表（最近7天）...")
    approval_list = get_approval_instances(token, size=5)
    
    if approval_list.get("errcode") == 0:
        result = approval_list.get("result", {})
        instance_ids = result.get("list", [])
        print(f"✅ 找到 {len(instance_ids)} 条审批记录")
        
        if instance_ids:
            print("\n审批实例 ID 列表:")
            for idx, instance_id in enumerate(instance_ids[:5], 1):
                print(f"  {idx}. {instance_id}")
                
                # 获取详情
                detail = get_approval_detail(token, instance_id)
                if detail.get("errcode") == 0:
                    process = detail.get("process_instance", {})
                    title = process.get("title", "无标题")
                    status = process.get("status", "未知")
                    originator = process.get("originator_userid", "未知")
                    print(f"     标题: {title} | 状态: {status} | 发起人: {originator}")
    else:
        print(f"❌ 获取审批列表失败: {approval_list.get('errmsg')}")
    
    # 3. 获取群列表
    print("\n[3] 获取群列表...")
    groups = get_chat_groups(token)
    
    if groups.get("errcode") == 0:
        chat_list = groups.get("chat_list", [])
        print(f"✅ 找到 {len(chat_list)} 个群")
        
        for idx, group in enumerate(chat_list[:3], 1):
            name = group.get("name", "未命名")
            chatid = group.get("chatid", "")
            print(f"  {idx}. {name} (ID: {chatid})")
    else:
        print(f"❌ 获取群列表失败: {groups.get('errmsg')}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)
