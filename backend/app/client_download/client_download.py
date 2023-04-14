from app.client_download import config
from pathlib import Path
from fastapi import HTTPException
import os
from app.service import info_data_service

async def client_download_file(Response, name, username):
    
    path= Path(f'{config.datafolder}/{name}.zip')
    if not path.exists():
        raise HTTPException(status_code=404, detail={"status": "Not found", "message": "File not found"})
    else:
        info = await info_data_service.InFoDataService.find_by_str(name)
        info_username = info.accountNo
        if info_username != username:
            raise HTTPException(
            status_code=403, detail={"status": "Forbidden" , "message": "Can not delete other user's data"}
        )
        else:
            content = path.read_bytes()
            response = Response(content, media_type="application/octet-stream")
            response.headers["Content-Disposition"] = f"attachment; filename={f'{name}.zip'}"
            return response

async def client_delete_file(names:list, username):
    for name in names:
        path= Path(f'{config.datafolder}/{name}.zip')
        if not path.exists():
            raise HTTPException(status_code=404, detail={"status": "Not found" , "message": "File not found"})
        else:
            info = await info_data_service.InFoDataService.find_by_str(name)
            info_username = info.accountNo
            if info_username != username:
                raise HTTPException(
                status_code=403, detail={"status": "Forbidden" , "message": "Can not delete other user's data"}
                                    )
            else:
                await info_data_service.InFoDataService.update_status_downloadable(name, True, False)
                return os.remove(path)