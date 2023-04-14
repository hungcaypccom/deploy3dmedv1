from app.model import Person, Users, UsersRole, Role

from app.repository.role import RoleRepository
from app.repository.user_role import UsersRoleRepository
from app.service.user_service import UserService



async def find_role(role_name: str):
    info = await RoleRepository.find_by_list_role_name(role_name)
    return info

async def find_role_users(role_name: str):
    info = await RoleRepository.find_by_role_name(role_name)
    return info

async def find_role_by_user_id(username_id):
    _usersRole = await UsersRoleRepository.find_by_user_id(username_id)
    _role = await RoleRepository.find_by_role_id(_usersRole.role_id)
    return _role


async def find_role_by_username(username):
    _username= await UserService.find_account(username)
    _usersRole = await UsersRoleRepository.find_by_user_id(_username.id)
    _role = await RoleRepository.find_by_role_id(_usersRole.role_id)
    return _role
