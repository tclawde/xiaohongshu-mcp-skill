#!/usr/bin/env bash
#
# 🦀 Xiaohongshu 一键登录脚本（修复版）
# 
# 修复：小红书更新了登录页面，需要从探索页面点击登录按钮
# 
# 用法: 
#   ./xhs_login.sh              # 仅登录
#   ./xhs_login.sh --notify    # 登录并发送二维码到飞书
#

set -e

# 配置
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
SCRIPTS_DIR="${WORKSPACE_DIR}/scripts"
COOKIES_PATH="${WORKSPACE_DIR}/cookies.json"

# 飞书用户 ID
FEISHU_USER="ou_715534dc247ce18213aee31bc8b224cf"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[✅]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[⚠️]${NC} $1"; }
log_error() { echo -e "${RED}[❌]${NC} $1"; }

# 截图功能
take_qr_screenshot() {
    log_info "等待二维码加载..."
    sleep 3
    
    # 使用 Playwright 截图（自动化方式）
    python3 "${SKILL_DIR}/scripts/xhs_login_screenshot.py" 2>/dev/null
    
    if [ -f "${WORKSPACE_DIR}/xhs_login_qr.png" ]; then
        log_success "截图成功"
        return 0
    fi
    
    log_warning "自动截图失败，将尝试手动操作"
    return 1
}

# 发送到飞书
send_to_feishu() {
    local screenshot="${WORKSPACE_DIR}/xhs_login_qr.png"
    
    if [ ! -f "$screenshot" ]; then
        log_warning "无截图，跳过发送"
        return 1
    fi
    
    log_info "发送二维码到飞书..."
    
    if command -v message &> /dev/null; then
        message --action send \
            --channel feishu \
            --target "${FEISHU_USER}" \
            --media "${screenshot}" \
            --message "🦀 **小红书登录二维码**\n\n请用小红书 App 扫码登录。\n\n扫码后回复'已登录'" \
            --caption "登录二维码"
        
        log_success "已发送二维码到飞书"
    else
        log_warning "message 工具不可用"
        log_info "截图位置: ${screenshot}"
    fi
}

# 检查 MCP 服务器
check_mcp_server() {
    if ! curl -s http://localhost:18060/api/v1/login/status &>/dev/null; then
        log_warning "MCP 服务器未运行，启动中..."
        cd "${WORKSPACE_DIR}"
        nohup ./xiaohongshu-mcp-darwin-arm64 > /tmp/xhs_mcp.log 2>&1 &
        sleep 3
    fi
    
    # 检查登录状态
    local status
    status=$(curl -s http://localhost:18060/api/v1/login/status | grep -o '"is_logged_in":true')
    
    if [ -n "$status" ]; then
        log_success "已无需重新登录！登录"
        return 1
    fi
    
    return 0
}

# 使用 Playwright 登录
playwright_login() {
    log_info "使用 Playwright 自动化登录..."
    
    cd "${SKILL_DIR}"
    
    # 检查依赖
    if ! python3 -c "from playwright" 2>/dev/null; then
        log_info "安装 Playwright..."
        pip3 install playwright --quiet
        playwright install chromium 2>/dev/null || true
    fi
    
    # 运行登录脚本
    python3 scripts/xhs_login_sop.py
    
    # 复制 cookies 到 MCP 读取位置
    if [ -f "${WORKSPACE_DIR}/xiaohongshu_cookies_live.json" ]; then
        cp "${WORKSPACE_DIR}/xiaohongshu_cookies_live.json" "${COOKIES_PATH}"
        log_success "Cookies 已保存"
    fi
    
    return 0
}

# 验证登录
verify_login() {
    log_info "验证登录状态..."
    
    sleep 2
    
    local status
    status=$(curl -s http://localhost:18060/api/v1/login/status | grep -o '"is_logged_in":true')
    
    if [ -n "$status" ]; then
        log_success "登录成功！"
        return 0
    else
        log_error "登录可能失败，请检查"
        return 1
    fi
}

# 主函数
main() {
    echo "================================"
    echo "  🦀 Xiaohongshu 一键登录（修复版）"
    echo "================================"
    echo ""
    echo "修复：小红书登录页面变更"
    echo "流程：探索页面 → 点击登录 → 扫码 → 保存 cookies"
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
                echo "  --help, -h      显示帮助"
                exit 0
                ;;
        esac
    done
    
    # 检查是否已登录
    if ! check_mcp_server; then
        exit 0
    fi
    
    # 如果需要通知，先截图发送
    if [ "$NOTIFY" = true ]; then
        # 启动 Playwright 登录（会自动截图发送）
        playwright_login
        verify_login
    else
        # 仅登录
        playwright_login
        verify_login
    fi
    
    echo ""
    echo "================================"
}

main "$@"
