import aiohttp
import aiofiles
import asyncio
import time
from fastapi import FastAPI
import pickle
import time

#config for API form hans's server

class Config:

    URL_login = "http://47.243.175.209:8080/EX-PRO/accLogin"
    URL_reset = "http://47.243.175.209:8080/EX-PRO/resetPwd"
    URL_getFileInfo = "http://47.243.175.209:8080/EX-PRO/api/file/getFileInfos"
    URL_download = "http://47.243.175.209:8080/EX-PRO/api/file/download"
    URL_cookies = "http://47.243.175.209:8080/EX-PRO"

    params = {
    "loginPwd": "loginPwd",
    "accountNo": "accountNo",
    "accessSource": "accessSource",
    "initPwd": "initPwd",
    "uploadTimeStr": "uploadTimeStr"
    }

# account to logging
    loginAccount = {
        "account": "191573222",
        "password": "e88b37af3c8c86ef15a267ee994be968",
        "accessSource": "pc"
    }

# indicating the path to storge data downloaded, must be same with the config file of client_download module
    datafolder = "datas"

