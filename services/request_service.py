"""HTTP请求服务模块"""
import os
import requests
from lxml import etree
from typing import Optional
from utils.logger import log
from utils.file_handler import save_file, save_js_content
import config


def download_js_file(js_path: str, js_name: str) -> None:
    """
    下载外链JS文件

    Args:
        js_path: JS文件的相对路径
        js_name: 保存的文件名
    """
    response = requests.get(
        config.BASE_URL + js_path,
        headers=config.JS_REQUEST_HEADERS,
    )
    # 使用绝对路径保存
    file_path = os.path.join(config.JS_FILES_DIR, js_name)
    save_file(file_path, response.content, mode='wb')
    log.info(f'成功获取外链js: {js_path}')


def request_first_page() -> str:
    """
    第一次请求，获取初始cookie和JS文件

    Returns:
        FSSBBIl1UgzbN7N80S cookie值
    """
    response = requests.get(
        config.TARGET_URL,
        headers=config.FIRST_REQUEST_HEADERS
    )

    html_text = etree.HTML(response.text)

    # 提取并保存content
    content = html_text.xpath('//meta[2]/@content')[0]
    save_js_content(
        os.path.join(config.JS_FILES_DIR, 'content.js'),
        content
    )

    # 保存script内容
    script = html_text.xpath('//head/script[2]/text()')[0]
    save_file(
        os.path.join(config.JS_FILES_DIR, 'func.js'),
        script,
        mode='wb',
        encoding='utf-8'
    )
    log.info('成功获取script的js代码：func.js')

    # 下载外链JS
    js_path = html_text.xpath('//head/script[1]/@src')[0]
    download_js_file(js_path, "ts.js")

    return response.cookies['FSSBBIl1UgzbN7N80S']


def verify_request(cookie_s: str, cookie_t: str) -> None:
    """
    验证请求，获取第二轮的JS文件

    Args:
        cookie_s: FSSBBIl1UgzbN7N80S cookie值
        cookie_t: FSSBBIl1UgzbN7N80T cookie值
    """
    cookies = {
        'FSSBBIl1UgzbN7N80S': cookie_s,
        'FSSBBIl1UgzbN7N80T': cookie_t,
    }

    response = requests.get(
        config.TARGET_URL,
        cookies=cookies,
        headers=config.VERIFY_REQUEST_HEADERS,
    )

    # 保存HTML文件到js_files目录
    save_file(
        os.path.join(config.JS_FILES_DIR, "new.html"),
        response.content,
        mode='wb'
    )

    html_text = etree.HTML(response.text)

    # 提取并保存content
    content = html_text.xpath('//meta[13]/@content')[0]
    save_js_content(
        os.path.join(config.JS_FILES_DIR, 'content2.js'),
        content
    )

    # 保存script内容
    script = html_text.xpath('//head/script[2]/text()')[0]
    save_file(
        os.path.join(config.JS_FILES_DIR, 'func2.js'),
        script,
        mode='wb',
        encoding='utf-8'
    )
    log.info('成功获取script中的js代码：func2.js')

    # 下载外链JS
    js_path = html_text.xpath('//head/script[1]/@src')[0]
    download_js_file(js_path, "ts2.js")


def fetch_data(cookie_s: str, cookie_t: str, mme_param: str) -> Optional[dict]:
    """
    获取最终数据

    Args:
        cookie_s: FSSBBIl1UgzbN7N80S cookie值
        cookie_t: FSSBBIl1UgzbN7N80T cookie值
        mme_param: MmEwMD参数

    Returns:
        API响应的JSON数据，如果失败返回None
    """
    cookies = {
        'FSSBBIl1UgzbN7N80S': cookie_s,
        'FSSBBIl1UgzbN7N80T': cookie_t,
    }

    params = {'MmEwMD': mme_param}

    data = {
        'pageNum': '1',
        'pageSize': '10',
        'searchTitle': '',
        'ishot': '1',
    }

    try:
        response = requests.post(
            config.API_URL,
            params=params,
            cookies=cookies,
            headers=config.API_REQUEST_HEADERS,
            data=data,
        )

        log.info(f"响应状态码: {response.status_code}")
        log.info(f"响应内容: {response.text}")

        # 检查HTTP状态码
        response.raise_for_status()

        # 尝试解析JSON
        return response.json()

    except requests.exceptions.JSONDecodeError as e:
        log.error(f"JSON解析失败: {e}")
        log.error(f"原始响应内容: {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        log.error(f"HTTP请求失败: {e}")
        return None
    except Exception as e:
        log.error(f"未知错误: {e}")
        return None
