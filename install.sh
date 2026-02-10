#!/usr/bin/env bash
#
# 🦀 Xiaohongshu MCP 一键安装脚本
#
# 从零复现完整环境
# 用法:
#   bash <(curl -s https://raw.githubusercontent.com/tclawde/xiaohongshu-mcp-skill/main/install.sh)
#

set -e

# 配置
SKILL_REPO="https://github.com/tclawde/xiaohongshu-mcp-skill.git"
SKILL_DIR="${HOME}/.openclaw/workspace/skills/xiaohongshu-mcp"
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
SCRIPTS_DIR="${WORKSPACE_DIR}/scripts"
MCP_VERSION="v0.0.5"
MCP_REPO_URL="https://github.com/xpzouying/xiaohongshu-mcp/releases"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
err() { echo -e "${RED}[ERROR]${NC} $1" >&2; }
success() { echo -e "${GREEN}[✅]${NC} $1"; }

# 检查系统
check_system() {
    log "检查系统环境..."
    
    if [[ "$(uname)" != "Darwin" ]]; then
        warn "本脚本主要针对 macOS 设计，Linux/Windows 可能需要手动调整"
    fi
    
    if ! command -v python3 &> /dev/null; then
        err "Python 3 未安装，请先安装 Python 3"
        exit 1
    fi
    
    success "系统检查通过"
}

# 创建目录结构
create_dirs() {
    log "创建目录结构..."
    
    mkdir -p "${SCRIPTS_DIR}"
    mkdir -p "${SKILL_DIR}/scripts"
    mkdir -p "${WORKSPACE_DIR}"
    
    success "目录创建完成"
}

# 从GitHub克隆或更新skill
clone_or_update_skill() {
    log "克隆/更新 Xiaohongshu MCP Skill..."
    
    if [ -d "${SKILL_DIR}/.git" ]; then
        log "Skill 已存在，更新中..."
        cd "${SKILL_DIR}"
        git pull origin main
    else
        log "从 GitHub 克隆..."
        git clone "${SKILL_REPO}" "${SKILL_DIR}"
    fi
    
    success "Skill 安装完成"
}

# 安装 Python 依赖
install_dependencies() {
    log "安装 Python 依赖..."
    pip3 install requests --quiet
    success "依赖安装完成"
}

# 安装 MCP 工具（二进制文件）
install_mcp_tools() {
    log "安装 MCP 工具..."
    
    cd "${WORKSPACE_DIR}"
    
    # 下载服务器
    if [ ! -f "xiaohongshu-mcp-darwin-arm64" ]; then
        log "下载 MCP 服务器..."
        curl -L -o "xiaohongshu-mcp-darwin-arm64" \
            "${MCP_REPO_URL}/${MCP_VERSION}/xiaohongshu-mcp-darwin-arm64"
        chmod +x "xiaohongshu-mcp-darwin-arm64"
    else
        warn "MCP 服务器已存在，跳过"
    fi
    
    # 下载登录工具
    if [ ! -f "xiaohongshu-login-darwin-arm64" ]; then
        log "下载登录工具..."
        curl -L -o "xiaohongshu-login-darwin-arm64" \
            "${MCP_REPO_URL}/${MCP_VERSION}/xiaohongshu-login-darwin-arm64"
        chmod +x "xiaohongshu-login-darwin-arm64"
    else
        warn "登录工具已存在，跳过"
    fi
    
    success "MCP 工具安装完成"
}

# 复制脚本到 scripts 目录
install_scripts() {
    log "安装脚本到 ${SCRIPTS_DIR}..."
    
    cp "${SKILL_DIR}/xhs_login.sh" "${SCRIPTS_DIR}/"
    cp "${SKILL_DIR}/xhs_client.py" "${SKILL_DIR}/scripts/"
    
    chmod +x "${SCRIPTS_DIR}/xhs_login.sh"
    chmod +x "${SKILL_DIR}/scripts/xhs_client.py"
    
    success "脚本安装完成"
}

# 验证安装
verify_install() {
    log "验证安装..."
    
    local errors=0
    
    # 检查文件
    [ -f "${WORKSPACE_DIR}/xiaohongshu-mcp-darwin-arm64" ] || { err "缺少 MCP 服务器"; ((errors++)); }
    [ -f "${WORKSPACE_DIR}/xiaohongshu-login-darwin-arm64" ] || { err "缺少登录工具"; ((errors++)); }
    [ -f "${SKILL_DIR}/scripts/xhs_client.py" ] || { err "缺少 Python 客户端"; ((errors++)); }
    [ -f "${SCRIPTS_DIR}/xhs_login.sh" ] || { err "缺少一键登录脚本"; ((errors++)); }
    
    # 检查 Python
    python3 -c "import requests" 2>/dev/null || { err "requests 库未安装"; ((errors++)); }
    
    if [ $errors -eq 0 ]; then
        success "安装验证通过！"
        return 0
    else
        err "安装验证失败，发现 ${errors} 个问题"
        return 1
    fi
}

# 打印使用说明
print_usage() {
    echo ""
    echo "========================================"
    echo "  🦀 Xiaohongshu MCP 安装完成！"
    echo "========================================"
    echo ""
    echo "📁 文件位置:"
    echo "   - Skill 目录: ${SKILL_DIR}"
    echo "   - MCP 工具: ${WORKSPACE_DIR}/"
    echo "   - Python 客户端: ${SKILL_DIR}/scripts/"
    echo "   - 一键脚本: ${SCRIPTS_DIR}/"
    echo ""
    echo "🚀 快速开始:"
    echo ""
    echo "1. 启动 MCP 服务器:"
    echo "   cd ${WORKSPACE_DIR}"
    echo "   ./xiaohongshu-mcp-darwin-arm64 &"
    echo ""
    echo "2. 登录:"
    echo "   bash ${SCRIPTS_DIR}/xhs_login.sh --notify"
    echo ""
    echo "3. 使用:"
    echo "   python3 ${SKILL_DIR}/scripts/xhs_client.py status"
    echo "   python3 ${SKILL_DIR}/scripts/xhs_client.py search \"咖啡\""
    echo ""
    echo "📖 文档:"
    echo "   - ${SKILL_DIR}/README.md"
    echo "   - ${SKILL_DIR}/SOP.md"
    echo ""
    echo "🔗 GitHub:"
    echo "   https://github.com/tclawde/xiaohongshu-mcp-skill"
    echo ""
}

# 主函数
main() {
    echo "========================================"
    echo "  🦀 Xiaohongshu MCP 一键安装脚本"
    echo "========================================"
    echo ""
    echo "从零复现完整环境..."
    echo ""
    
    check_system
    create_dirs
    clone_or_update_skill
    install_dependencies
    install_mcp_tools
    install_scripts
    
    echo ""
    if verify_install; then
        print_usage
    else
        warn "请检查上述错误"
    fi
}

main "$@"
