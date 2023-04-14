import aiohttp
import aiofiles
import time
from fastapi import FastAPI
import pickle
import time



from app.hans3d.config import Config

class Connect: 

    @staticmethod    
    async def takeCookies():
        async with aiohttp.ClientSession() as session:
            resp = await session.get(Config.URL_cookies)
        pickle.dump(resp.cookies, open("cookies.pkl", "wb"))

    @staticmethod
    async def fetch(session, url, param, timeout):
        s_cookies = pickle.load(open("cookies.pkl", "rb"))
        try:
            async with session.post(url, params = param, cookies = s_cookies, timeout = timeout) as response: 
                return await response.json()
        except Exception as er:
            return repr(er)
    @staticmethod
    async def fetchDownload(session, url, param, name, timeout):
        s = time.perf_counter()
        s_cookies = pickle.load(open("cookies.pkl", "rb"))
        try:
            async with session.get(url, params = param, cookies = s_cookies, allow_redirects=True, timeout = timeout) as response:
                print(session)
                f = await aiofiles.open(f'{Config.datafolder}/{name}.zip', mode='wb')
                await f.write(await response.read())
                await f.close()
            elapsed = time.perf_counter() - s
            print(elapsed)
            return True
        except Exception as er:
            return False
        
        



        

