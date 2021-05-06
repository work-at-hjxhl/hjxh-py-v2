from log import logger

COOKIE = '''// Semicolon separated Cookie File
// This file was generated by EditThisCookie
// Details: http://www.ietf.org/rfc/rfc2109.txt
// Example: http://www.tutorialspoint.com/javascript/javascript_cookies.htm
_nano_fp=pEalpCjlpEYXqdjn9_bn7ZFBW6yuyeLtaXMCztW;SUB_PASS_ID=eyJ0Ijoic0FJZHVLOERDNVRsS2xNL1lESU5PV2ErT1pGMlJhY3ArUGVlWmV2Nk9pQTk5Q0dkanYzbEtlaEVQMi9rdDlLNCIsInYiOjEsInMiOjcsIm0iOjUwNjY3Mzk3MCwidSI6OTM5MTc4OTJ9'''


def verify_cookie(cookie: str):
    """
    最重要的两个字段是 _nano_fp 和 SUB_PASS_ID
    """
    import subprocess
    
    import requests
    
    UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    URL_GET_PDD_USER_INFO = "https://yingxiao.pinduoduo.com/mms-gateway/user/info"
    
    cookie = [i for i in cookie.splitlines() if i][-1]
    
    anti_content = subprocess.check_output(['node', '../nodejs/hack_anti-content_from_cookie.js', cookie],
                                           encoding='utf-8').strip()
    
    data = {
        'crawlerInfo': anti_content,
        'mallId': None
    }
    
    headers = {
        'anti-content': anti_content,
        'user-agent': UA,
        'COOKIE': cookie
    }
    
    userinfo = requests.post(URL_GET_PDD_USER_INFO, data=data, headers=headers).json()  # type: dict
    if userinfo['error_code'] != 1000:
        raise ValueError('登录失败：', userinfo)
    if not userinfo['result']['hasLogin']:
        raise ValueError('该账号尚未登录：', userinfo)
    return userinfo


def verify_username_cookie(username: str, cookie: str):
    userinfo = verify_cookie(cookie)
    username2 = userinfo['result']['username']
    if username != username2:
        raise ValueError(f'username不匹配，输入的username: {username}, cookie对应的username: {username2}')


def verify_user(username: str, password: str, cookie: str) -> bool:
    logger.warning('todo: verification of password support')
    """
    todo: 校验password
    """
    try:
        verify_username_cookie(username, cookie)
    except Exception as e:
        logger.error(e)
        logger.info('校验失败！')
        return False
    else:
        logger.info('校验通过！')
        return True


if __name__ == '__main__':
    verify_user('乐和食品店:冯露', '', COOKIE)