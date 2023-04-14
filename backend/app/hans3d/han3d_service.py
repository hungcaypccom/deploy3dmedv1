import aiohttp


from app.hans3d.config import Config
from app.hans3d.connect import Connect

params_getFileInfo = { 'accountNo': '994985849' }
params_download = { 'uploadTimeStr' : '20210301193624259' , 
'accountNo': '994985849' }


class Service(Connect):

   
    @staticmethod
    async def login(timeout):
        param = {
            Config.params["loginPwd"] : Config.loginAccount["password"], 
            Config.params["accountNo"]: Config.loginAccount["account"],
            Config.params["accessSource"]: Config.loginAccount["accessSource"]
        }
        async with aiohttp.ClientSession() as session:
            resp = await Connect.fetch(session, Config.URL_login, param, timeout)
            return resp

    @staticmethod
    async def reset(timeout):
        param = {
            Config.params["initPwd"] : Config.loginAccount["password"], 
            Config.params["accountNo"]: Config.loginAccount["account"]  
        }
        async with aiohttp.ClientSession() as session:
            return await Connect.fetch(session, Config.URL_reset, param, timeout)
        
    @staticmethod     
    async def getInfoData(account, timeout):
        param = {
            Config.params["accountNo"] : account
        }
        async with aiohttp.ClientSession() as session:
            return await Connect.fetch(session, Config.URL_getFileInfo, param, timeout)
         
    @staticmethod     
    async def download(uploadTimeStr, account, timeout):
        param = {
            Config.params["uploadTimeStr"] : uploadTimeStr,
            Config.params["accountNo"] : account,
        }
        async with aiohttp.ClientSession() as session:
            return await Connect.fetchDownload(session, Config.URL_download, param, uploadTimeStr, timeout)


"""async def main(url):
    async with aiohttp.ClientSession() as session:
        resp = await fetch(session, url)
        print(resp)


async def get_all(session, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results
    



async def fetch(session, url):
    async with session.get(url) as response:
        print(response.cookies)
        return  response


async def connect(url):
    async with aiohttp.ClientSession() as session:
       resp = await fetch(session, url)
       print(await resp.read())
       
   
           


@app.get('/login')
async def f():
     await takeCookies()
     async with aiohttp.ClientSession() as session:
        resp = await fetch(session, URL_login)
        print(resp)
        

@app.get('/reset')
async def f():
    async with aiohttp.ClientSession() as session:
        resp = await fetch(session, URL_reset)
        print(resp)


@app.get('/info')
async def f():
    async with aiohttp.ClientSession() as session:
        resp = await fetch(session, URL_getFileInfo[2])
        return(resp)

@app.get('/download')
async def f():
    s = time.perf_counter()
    i=0
    tasks = []
    async with aiohttp.ClientSession() as session:  
        for url in urls:
            task = asyncio.create_task(fetchDownload(session, url, name[i]))
            print(task)
            tasks.append(task)
            i=i+1
        results = await asyncio.gather(*tasks)
        elapsed = time.perf_counter() - s
        print(elapsed)
        

@app.get('/test')
async def f():
    s = time.perf_counter()
    i=0
    async with aiohttp.ClientSession() as session:  
        for url in urls:
            task = await fetchDownload(session, url, name[i])
            i=i+1
        elapsed = time.perf_counter() - s
        print(elapsed)
    
    """