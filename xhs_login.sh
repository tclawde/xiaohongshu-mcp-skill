#!/usr/bin/env bash
#
# 🦀 Xiaohongshu 一键登录脚本
# 
# 用法: 
#   ./xhs_login.sh              # 仅登录
#   ./xhs_login.sh --notify    # 登录并发送二维码到飞书
#

set -e

# 配置
WORKSPACE="/Users/apple/.openclaw/workspace"
SCRIPTS_DIR="${WORKSPACE}/scripts"
LOGIN_TOOL="${WORKSPACE}/xiaohongshu-login-darwin-arm64"
CLIENT_SCRIPT="${WORKSPACE}/skills/xiaohongshu-mcp/scripts/xhs_client.py"
QR_SCREENSHOT="${HOME}/Desktop/xhs_qr.png"

# 飞书配置
FEISHU_USER="ou_715534dc247ce18213aee31bc8b224cf"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[✅]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠️]${NC} $1"
}

log_error() {
    echo -e "${RED}[❌]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."
    
    # 检查登录工具
    if [ ! -f "${LOGIN_TOOL}" ]; then
        log_error "登录工具不存在: ${LOGIN_TOOL}"
        log_info "请从以下地址下载:"
        log_info "  https://github.com/xpzouying/xiaohongshu-mcp/releases"
        exit 1
    fi
    
    # 检查 MCP 客户端
    if [ ! -f "${CLIENT_SCRIPT}" ]; then
        log_error "MCP 客户端不存在: ${CLIENT_SCRIPT}"
        exit 1
    fi
    
    # 检查 MCP 服务器
    if ! ps aux | grep -v grep | grep -q "xiaohongshu-mcp"; then
        log_warning "MCP 服务器未运行，尝试启动..."
        cd "${WORKSPACE}"
        nohup ./xiaohongshu-mcp-darwin-arm64 > /tmp/xhs_mcp.log 2>&1 &
        sleep 3
        log_info "MCP 服务器已启动"
    fi
    
    log_success "依赖检查通过"
}

# 截图功能
take_qr_screenshot() {
    log_info "截取二维码..."
    
    # 尝试多种截图方式
    if command -v screencapture &> /dev/null; then
        # 方式1: screencapture
        if /usr/sbin/screencapture -x "${QR_SCREENSHOT}" 2>/dev/null; then
            if [ -s "${QR_SCREENSHOT}" ]; then
                log_success "截图成功: ${QR_SCREENSHOT}"
                return 0
            fi
        fi
    fi
    
    log_warning "截图失败，将跳过截图步骤"
    return 1
}

# 发送到飞书
send_to_feishu() {
    if ! take_qr_screenshot; then
        log_warning "跳过发送到飞书（无截图）"
        return 1
    fi
    
    log_info "发送二维码到飞书..."
    
    # 使用 OpenClaw message 工具
    if command -v message &> /dev/null; then
        message --action send \
            --channel feishu \
            --target "user:${FEISHU_USER}" \
            --file "${QR_SCREENSHOT}" \
            --message "🦀 小红书登录二维码！\n\n请用小红书 App 扫码登录。\n\n登录成功后告诉我～" \
            --caption "小红书登录二维码"
        
        log_success "已发送二维码到飞书"
    else
        log_warning "message 工具不可用，请手动发送截图"
        log_info "截图位置: ${QR_SCREENSHOT}"
    fi
}

# 启动登录
start_login() {
    log_info "启动小红书登录..."
    log_info "请用小红书 App 扫描弹出的二维码"
    
    cd "${WORKSPACE}"
    
    # 启动登录工具
    "${LOGIN_TOOL}"
}

# 验证登录
verify_login() {
    log_info "验证登录状态..."
    
    if python3 "${CLIENT_SCRIPT}" status; then
        log_success "登录成功！"
        return 0
    else
        log_error "登录失败或超时"
        return 1
    fi
}

# 主函数
main() {
    echo "================================"
    echo "  🦀 Xiaohongshu 一键登录脚本"
    echo "================================"
    echo ""
    
    NOTIFY=false
    for arg in "$@"; do
        case $arg in
            --notify|-n)
                NOTIFY=true
                ;;
            --help|-h)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --notify, -n   登录并发送二维码到飞书"
                echo "  --help, -h     显示帮助信息"
                exit 0
                ;;
        esac
    done
    
    # 检查依赖
    check_dependencies
    
    # 如果需要通知，先截图发送
    if [ "$NOTIFY" = true ]; then
        # 先启动登录工具（在后台）
        log_info "启动登录工具（在后台）..."
        cd "${WORKSPACE}"
        "${LOGIN_TOOL}" > /tmp/xhs_login.log 2>&1 &
        LOGIN_PID=$!
        
        sleep 5
        
        # 截图并发送
        send_to_feishu
        
        # 等待登录完成
        log_info "等待登录完成（请扫码）..."
        wait $LOGIN_PID 2>/dev/null || true
        
        # 验证
        verify_login
    else
        # 仅登录
        start_login
        verify_login
    fi
    
    echo ""
    echo "================================"
}

# 执行主函数
main "$@"
