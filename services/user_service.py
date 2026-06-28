from dto import CredentialsDTO, UserDTO, UserUpdateDTO
from repositories.user_repository import UserRepository
from exceptions import UserExistsException, UserNotFoundException

class UserService:
    async def create_user(self, credentials: CredentialsDTO) -> UserDTO:
        user_repository = UserRepository()

        existing_id = await user_repository.get_user_id_by_login(credentials.login)

        if existing_id:
            raise UserExistsException()
        
        user = await user_repository.create_user(credentials)

        return UserDTO(**user.model_dump())
        
    async def get_user(self, search_by: dict, with_relations: bool) -> UserDTO:
        user = await UserRepository().get_user(search_by, with_relations)

        if not user:
            raise UserNotFoundException()

        return UserDTO(**user.model_dump())
    
    async def get_users(self, search_by: dict, with_relations: bool) -> list[UserDTO]:
        users = await UserRepository().get_users(search_by, with_relations)

        return [UserDTO(**user.model_dump()) for user in users]

    async def update_user(self, search_by: dict, user: UserUpdateDTO) -> UserDTO:
        user_repository = UserRepository()

        existing_user = await user_repository.get_user(search_by)

        if not existing_user:
            raise UserNotFoundException()

        updated_user = await user_repository.update_user(
            search_by, 
            user.model_dump(exclude_unset=True)
        )

        return UserDTO(**updated_user.model_dump())

    async def delete_user(self, search_by: dict, soft_delete: bool) -> None:
        user_repository = UserRepository()

        user = await user_repository.get_user(search_by)

        if not user:
            raise UserNotFoundException()
        
        await user_repository.delete_user(search_by, soft_delete)