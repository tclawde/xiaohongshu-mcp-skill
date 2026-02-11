#!/usr/bin/env python3
"""
小红书登录 SOP - 修复版

问题：小红书更新了登录页面，/user/account/login 返回维护页面
解决：从探索页面点击登录按钮触发二维码弹窗
"""

import asyncio
import json
import os
import sys
from pathlib import Path

from playwright.async_api import async_playwright

WORKSPACE_DIR = Path.home() / ".openclaw" / "workspace"

def save_cookies_to_all_locations(cookies):
    """保存 cookies 到所有 MCP 可能读取的位置"""
    cookies_json = json.dumps(cookies, indent=2)
    
    paths = [
        WORKSPACE_DIR / "cookies.json",              # MCP 默认位置
        WORKSPACE_DIR / "xiaohongshu_cookies_live.json",  # 备份
        Path("/tmp/cookies.json"),                   # 旧路径兼容
    ]
    
    for p in paths:
        try:
            with open(p, 'w') as f:
                f.write(cookies_json)
            print(f"💾 Cookies 已保存: {p}")
        except Exception as e:
            print(f"⚠️ 保存失败 {p}: {e}")

async def login_and_notify():
    """登录并截图发送到飞书 - 修复版"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = await context.new_page()

        print("\n" + "=" * 50)
        print("  🦀 小红书自动登录（修复版）")
        print("  修复：从探索页面点击登录按钮")
        print("=" * 50 + "\n")

        # 1. 导航到探索页面
        print("🚀 导航到探索页面...")
        await page.goto("https://www.xiaohongshu.com/explore")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(2)

        # 2. 检查是否已登录
        if await check_login_status(page):
            print("✅ 已登录！保存 cookies...")
            cookies = await context.cookies()
            save_cookies_to_all_locations(cookies)
            await browser.close()
            return True

        # 3. 点击登录按钮
        print("👆 点击登录按钮...")
        login_selectors = [
            "text=登录",
            "button:has-text('登录')",
            ".login-btn",
            "[class*='login']",
            ".user-name"
        ]
        for selector in login_selectors:
            try:
                btn = await page.query_selector(selector)
                if btn:
                    await btn.click()
                    print(f"✅ 点击了: {selector}")
                    break
            except:
                continue

        # 4. 等待二维码出现
        print("⏳ 等待二维码加载...")
        await asyncio.sleep(3)

        # 5. 截图
        print("📸 截图...")
        screenshot_path = WORKSPACE_DIR / "xhs_login_qr.png"
        await page.screenshot(path=str(screenshot_path))

        # 6. 发送到飞书
        try:
            os.system(f'''
                openclaw message send --channel feishu \
                    --target "ou_715534dc247ce18213aee31bc8b224cf" \
                    --media "{screenshot_path}" \
                    --message "🦀 **小红书登录二维码**\n\n请扫码登录，完成后回复'已登录'"
            ''')
            print("✅ 已发送到飞书")
        except:
            print("⚠️ 发送飞书失败")

        print("\n📱 请扫码登录...")
        print("   打开小红书 App → 扫描二维码\n")

        # 7. 等待用户确认
        input("⏳ 扫码完成后按 Enter 继续...")

        # 8. 检查并保存 cookies
        cookies = await context.cookies()
        save_cookies_to_all_locations(cookies)
        
        await browser.close()
        return True

async def check_login_status(page) -> bool:
    """检查是否已登录"""
    logged_in_selectors = [
        ".main-container .user .link-wrapper .channel",
        ".user-name",
        "[class*='user'] [class*='avatar']",
    ]
    for selector in logged_in_selectors:
        try:
            el = await page.query_selector(selector)
            if el:
                return True
        except:
            continue
    return False

async def take_screenshot_only():
    """仅截图（供外部调用）"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.goto("https://www.xiaohongshu.com/explore")
        await asyncio.sleep(2)
        
        screenshot_path = WORKSPACE_DIR / "xhs_login_qr.png"
        await page.screenshot(path=str(screenshot_path))
        print(f"📸 截图已保存: {screenshot_path}")
        
        await browser.close()

if __name__ == "__main__":
    # 如果作为截图脚本调用
    if "--screenshot" in sys.argv:
        asyncio.run(take_screenshot_only())
    else:
        asyncio.run(login_and_notify())
