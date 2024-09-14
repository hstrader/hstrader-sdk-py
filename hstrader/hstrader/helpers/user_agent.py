import platform


def get_user_agent() -> str:
    os = platform.system()
    if os == "Windows":
        os = "Windows NT"
    os_version = platform.release()
    python_version = platform.python_version()
    hostname = platform.node()
    return f"PythonSDK/1.0.0 ({os} {os_version}) {hostname} Python {python_version}"


__USER_AGENT__ = get_user_agent()
