"""主程序入口"""
from utils.logger import log
from services.request_service import (
    request_first_page,
    verify_request,
    fetch_data
)
from services.js_executor import (
    execute_first_cookie_generation,
    execute_second_cookie_generation
)


def main():
    """主流程"""
    # 第一步：获取初始cookie
    log.info("=" * 50)
    log.info("开始第一步：请求初始页面")
    log.info("=" * 50)
    cookie_s = request_first_page()
    log.info(f'成功获取 FSSBBIl1UgzbN7N80S: {cookie_s}')

    # 第二步：生成第一个cookie
    log.info("\n" + "=" * 50)
    log.info("开始第二步：生成第一个cookie")
    log.info("=" * 50)
    cookie_t = execute_first_cookie_generation()
    log.info(f'成功获取 FSSBBIl1UgzbN7N80T: {cookie_t}')

    # 第三步：验证请求
    log.info("\n" + "=" * 50)
    log.info("开始第三步：验证请求")
    log.info("=" * 50)
    verify_request(cookie_s, cookie_t)

    # 第四步：生成最终cookie和参数
    log.info("\n" + "=" * 50)
    log.info("开始第四步：生成最终cookie和参数")
    log.info("=" * 50)
    cookie_t, mme_param = execute_second_cookie_generation(cookie_t)
    log.info(f'成功获取最终 FSSBBIl1UgzbN7N80T: {cookie_t}')
    log.info(f'成功获取 MmEwMD: {mme_param}')

    # 第五步：获取数据
    log.info("\n" + "=" * 50)
    log.info("开始第五步：获取最终数据")
    log.info("=" * 50)
    result = fetch_data(cookie_s, cookie_t, mme_param)

    log.info("\n" + "=" * 50)
    log.info("流程完成！")
    log.info("=" * 50)

    return result


if __name__ == '__main__':
    main()

