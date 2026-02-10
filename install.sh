#!/usr/bin/env bash
#
# 🦀 Xiaohongshu MCP 安装脚本
#
# 用法:
#   ./install.sh              # 交互式安装
#   ./install.sh --quick      # 快速安装（不下载工具）
#

set -e

# 配置
REPO_URL="https://github.com/xpzouying/xiaohongshu-mcp/releases"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${HOME}/.openclaw/workspace/skills"
WORKSPACE_DIR="${HOME}/.openclaw/workspace"
SCRIPTS_DIR="${WORKSPACE_DIR}/scripts"
MCP_TOOLS_DIR="${WORKSPACE_DIR}"

# 版本（从 xiaohongshu-mcp 最新版本）
MCP_VERSION="v0.0.5"
MCP_SERVER="xiaohongshu-mcp-darwin-arm64"
MCP_LOGIN="xiaohongshu-login-darwin-arm64"

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
    
    # 检查 macOS
    if [[ "$(uname)" != "Darwin" ]]; then
        warn "本脚本主要针对 macOS 设计，Linux/Windows 可能需要手动调整"
    fi
    
    # 检查 Python
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
    mkdir -p "${SKILLS_DIR}/xiaohongshu-mcp/scripts"
    mkdir -p "${MCP_TOOLS_DIR}"
    
    success "目录创建完成"
}

# 下载 MCP 工具
download_mcp_tools() {
    log "下载 MCP 工具..."
    
    cd "${MCP_TOOLS_DIR}"
    
    # 下载服务器
    if [ ! -f "${MCP_SERVER}" ]; then
        log "下载 MCP 服务器..."
        curl -L -o "${MCP_SERVER}" \
            "${REPO_URL}/${MCP_VERSION}/${MCP_SERVER}"
        chmod +x "${MCP_SERVER}"
    else
        warn "MCP 服务器已存在，跳过下载"
    fi
    
    # 下载登录工具
    if [ ! -f "${MCP_LOGIN}" ]; then
        log "下载登录工具..."
        curl -L -o "${MCP_LOGIN}" \
            "${REPO_URL}/${MCP_VERSION}/${MCP_LOGIN}"
        chmod +x "${MCP_LOGIN}"
    else
        warn "登录工具已存在，跳过下载"
    fi
    
    success "MCP 工具下载完成"
}

# 安装 Python 依赖
install_dependencies() {
    log "安装 Python 依赖..."
    
    pip3 install requests --quiet
    
    success "依赖安装完成"
}

# 安装增强版客户端
install_client() {
    log "安装增强版 Python 客户端..."
    
    # 复制客户端脚本
    cp "${SCRIPT_DIR}/xhs_client.py" \
       "${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py"
    
    # 设置执行权限
    chmod +x "${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py"
    
    success "Python 客户端安装完成"
}

# 安装一键登录脚本
install_login_script() {
    log "安装一键登录脚本..."
    
    cp "${SCRIPT_DIR}/xhs_login.sh" "${SCRIPTS_DIR}/xhs_login.sh"
    chmod +x "${SCRIPTS_DIR}/xhs_login.sh"
    
    success "一键登录脚本安装完成"
}

# 复制文档
install_docs() {
    log "安装文档..."
    
    cp "${SCRIPT_DIR}/README.md" "${SKILLS_DIR}/xiaohongshu-mcp/README.md"
    cp "${SCRIPT_DIR}/SOP.md" "${SKILLS_DIR}/xiaohongshu-mcp/SOP.md"
    
    success "文档安装完成"
}

# 创建快捷方式
create_alias() {
    log "创建快捷命令..."
    
    # 添加到 .zshrc 或 .bashrc
    RC_FILE="${HOME}/.zshrc"
    if [ ! -f "${RC_FILE}" ]; then
        RC_FILE="${HOME}/.bashrc"
    fi
    
    # 添加 alias
    ALIAS_LINE="# Xiaohongshu MCP\nalias xhs-status='python3 ${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py status'\nalias xhs-login='python3 ${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py login'\nalias xhs-search='python3 ${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py search'\nalias xhs-publish='python3 ${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py publish'"
    
    if ! grep -q "xhs-status" "${RC_FILE}" 2>/dev/null; then
        echo -e "\n${ALIAS_LINE}" >> "${RC_FILE}"
        success "已添加快捷命令到 ${RC_FILE}"
    else
        warn "快捷命令已存在，跳过"
    fi
}

# 验证安装
verify_install() {
    log "验证安装..."
    
    local errors=0
    
    # 检查文件
    [ -f "${MCP_TOOLS_DIR}/${MCP_SERVER}" ] || { err "缺少 MCP 服务器"; ((errors++)); }
    [ -f "${MCP_TOOLS_DIR}/${MCP_LOGIN}" ] || { err "缺少登录工具"; ((errors++)); }
    [ -f "${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py" ] || { err "缺少 Python 客户端"; ((errors++)); }
    [ -f "${SCRIPTS_DIR}/xhs_login.sh" ] || { err "缺少一键登录脚本"; ((errors++)); }
    
    # 检查 Python
    python3 -c "import requests" 2>/dev/null || { err "requests 库未安装"; ((errors++)); }
    
安装"; ((errors    if [ $errors -eq 0 ]; then
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
    echo "   - MCP 工具: ${MCP_TOOLS_DIR}/"
    echo "   - Python 客户端: ${SKILLS_DIR}/xiaohongshu-mcp/scripts/"
    echo "   - 一键脚本: ${SCRIPTS_DIR}/"
    echo ""
    echo "🚀 快速开始:"
    echo ""
    echo "1. 启动 MCP 服务器:"
    echo "   cd ${MCP_TOOLS_DIR}"
    echo "   ./${MCP_SERVER} &"
    echo ""
    echo "2. 登录:"
    echo "   bash ${SCRIPTS_DIR}/xhs_login.sh --notify"
    echo ""
    echo "3. 使用:"
    echo "   python3 ${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py status"
    echo "   python3 ${SKILLS_DIR}/xiaohongshu-mcp/scripts/xhs_client.py search \"咖啡\""
    echo ""
    echo "📖 文档:"
    echo "   - README: ${SKILLS_DIR}/xiaohongshu-mcp/README.md"
    echo "   - SOP: ${SKILLS_DIR}/xiaohongshu-mcp/SOP.md"
    echo ""
}

# 主函数
main() {
    local quick=false
    for arg in "$@"; do
        case $arg in
            --quick|-q) quick=true ;;
            --help|-h)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --quick, -q   快速安装（不下载 MCP 工具）"
                echo "  --help, -h    显示帮助"
                exit 0
                ;;
        esac
    done
    
    echo "========================================"
    echo "  🦀 Xiaohongshu MCP 安装脚本"
    echo "========================================"
    echo ""
    
    check_system
    create_dirs
    
    if [ "$quick" = false ]; then
        download_mcp_tools
    else
        warn "快速安装模式，跳过 MCP 工具下载"
    fi
    
    install_dependencies
    install_client
    install_login_script
    install_docs
    create_alias
    
    echo ""
    if verify_install; then
        print_usage
    else
        warn "请检查上述错误"
    fi
}

main "$@"
