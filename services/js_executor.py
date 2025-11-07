"""JS执行服务模块"""
import os
import re
from typing import Tuple
from py_mini_racer import MiniRacer
from utils.logger import log
from utils.file_handler import read_file
from utils.cookie_parser import parse_cookie_value
import config


def execute_first_cookie_generation() -> str:
    """
    执行第一轮JS生成cookie

    Returns:
        FSSBBIl1UgzbN7N80T cookie值
    """
    ctx = MiniRacer()

    # 1. 设置环境
    log.info("--- 1. 正在设置JS沙箱环境... ---")
    setup_code = read_file(os.path.join(config.JS_FILES_DIR, 'setup_env.js'))
    ctx.eval(setup_code)

    # 2. 执行content.js
    log.info("--- 2. 正在执行 content.js... ---")
    content_code = read_file(os.path.join(config.JS_FILES_DIR, 'content.js'))
    ctx.eval(content_code)

    # 3. 连接meta和content
    ctx.eval('meta1.content = content;')

    # 4. 执行ts.js
    log.info("--- 3. 正在执行 ts.js... ---")
    ts_code = read_file(os.path.join(config.JS_FILES_DIR, 'ts.js'))
    ctx.eval(ts_code)

    # 5. 执行func.js
    log.info("--- 4. 正在执行 func.js... ---")
    func_code = read_file(os.path.join(config.JS_FILES_DIR, 'func.js'))
    ctx.eval(func_code)

    # 6. 获取cookie
    log.info("--- 5. 获取最终的 Cookie... ---")
    cookie_full = ctx.eval('document.cookie')

    return parse_cookie_value(cookie_full)


def execute_second_cookie_generation(cookie_t: str) -> Tuple[str, str]:
    """
    执行第二轮JS生成cookie和MmEwMD参数

    Args:
        cookie_t: 第一轮获取的FSSBBIl1UgzbN7N80T值

    Returns:
        (新的cookie值, MmEwMD参数)
    """
    ctx = MiniRacer()

    # 1. 设置环境并替换cookie
    log.info("--- 1. 正在设置JS沙箱环境... ---")
    setup_code = read_file(os.path.join(config.JS_FILES_DIR, 'setup_env2.js'))

    # 替换cookie值
    pattern = r"document\.cookie = '[^']*'"
    replacement = f"document.cookie = 'FSSBBIl1UgzbN7N80T={cookie_t}'"
    setup_code = re.sub(pattern, replacement, setup_code)

    ctx.eval(setup_code)
    log.info("环境设置完成")

    # 2. 执行content2.js
    log.info("--- 2. 正在执行 content2.js... ---")
    content_code = read_file(os.path.join(config.JS_FILES_DIR, 'content2.js'))
    ctx.eval(content_code)

    # 3. 连接meta和content
    log.info("--- 3. 连接 meta1.content 和 content... ---")
    ctx.eval('meta1.content = content;')

    # 4. 执行ts2.js
    log.info("--- 4. 正在执行 ts2.js... ---")
    ts_code = read_file(os.path.join(config.JS_FILES_DIR, 'ts2.js'))
    ctx.eval(ts_code)

    # 5. 执行func2.js
    log.info("--- 5. 正在执行 func2.js... ---")
    func_code = read_file(os.path.join(config.JS_FILES_DIR, 'func2.js'))
    ctx.eval(func_code)

    # 6. 获取cookie
    log.info("--- 6. 获取最终的 Cookie... ---")
    cookie_full = ctx.eval('document.cookie')
    log.info(f'获取到的完整cookie: {cookie_full}')

    # 7. 获取MmEwMD参数
    log.info("--- 7. 获取 MmEwMD 参数... ---")
    mme_param = ''
    try:
        ctx.eval('''
            var g = new XMLHttpRequest();
            g.open("POST", "https://www.cde.org.cn/main/news/getHotNewsList", true);
        ''')

        req_param = ctx.eval('req_param')
        log.info(f'req_param 内容: {req_param}')

        if req_param:
            match = re.search(r'[?&]MmEwMD=([^&]+)', req_param)
            mme_param = match.group(1) if match else ''
            log.info(f'成功提取 MmEwMD: {mme_param}')
        else:
            log.warning('req_param 为空')
    except Exception as e:
        log.error(f'获取 MmEwMD 失败: {e}')

    # 8. 解析cookie值
    log.info("--- 8. 解析 Cookie 值... ---")
    cookie_value = parse_cookie_value(cookie_full)

    log.info(f'最终 cookie 值: {cookie_value}')
    log.info(f'最终 MmEwMD 值: {mme_param}')

    return cookie_value, mme_param
