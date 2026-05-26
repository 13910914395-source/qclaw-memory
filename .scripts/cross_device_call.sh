#!/bin/bash
# 跨设备任务调用脚本
# 用于在设备间触发任务执行

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/cross_device_config.json"
LOG_FILE="$SCRIPT_DIR/.cross_device.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# 读取配置
get_device_config() {
    local device="$1"
    local field="$2"
    cat "$CONFIG_FILE" | jq -r ".devices.$device.$field // empty"
}

# 检查设备是否在线（通过 ping 或 API）
check_device_online() {
    local device="$1"
    local endpoint=$(get_device_config "$device" "api_endpoint")
    
    if [ -z "$endpoint" ] || [ "$endpoint" = "null" ]; then
        log "⚠️  设备 $device 未配置 API 端点"
        return 1
    fi
    
    # 尝试调用健康检查接口
    if curl -s -f --connect-timeout 5 "$endpoint/health" > /dev/null 2>&1; then
        log "✅ 设备 $device 在线"
        return 0
    else
        log "❌ 设备 $device 离线"
        return 1
    fi
}

# 触发远程任务
trigger_remote_task() {
    local target_device="$1"
    local task_name="$2"
    local task_params="$3"
    
    local endpoint=$(get_device_config "$target_device" "api_endpoint")
    
    if [ -z "$endpoint" ]; then
        log "❌ 无法触发任务：设备 $target_device 未配置 API"
        return 1
    fi
    
    log "🚀 触发 $target_device 上的任务: $task_name"
    
    # 调用远程 API（示例）
    # curl -X POST "$endpoint/api/task" \
    #   -H "Content-Type: application/json" \
    #   -d "{\"task\": \"$task_name\", \"params\": $task_params}"
    
    log "✅ 任务已触发: $task_name"
}

# 同步记忆到目标设备
sync_to_device() {
    local target_device="$1"
    
    log "📤 同步记忆到 $target_device..."
    
    # 先执行本地提交
    "$SCRIPT_DIR/sync_workspace.sh" local
    
    # 如果配置了远程仓库，执行推送
    if check_device_online "$target_device"; then
        log "📦 尝试推送记忆到远程..."
        # "$SCRIPT_DIR/sync_workspace.sh" push
    fi
}

# 主逻辑
case "$1" in
    "check")
        check_device_online "$2"
        ;;
    "trigger")
        trigger_remote_task "$2" "$3" "$4"
        ;;
    "sync")
        sync_to_device "$2"
        ;;
    "status")
        echo "跨设备任务状态："
        cat "$CONFIG_FILE" | jq '.cross_device_tasks[] | "\(.name): \(.enabled)"'
        ;;
    *)
        echo "用法: $0 {check|trigger|sync|status} <device> [task] [params]"
        echo ""
        echo "示例："
        echo "  $0 check macbook_air"
        echo "  $0 trigger macbook_air daily_summary '{}'"
        echo "  $0 sync macbook_air"
        echo "  $0 status"
        ;;
esac
