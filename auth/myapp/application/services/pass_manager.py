from passlib.context import CryptContext
from pwdlib import PasswordHash

from myapp.application.interface.pass_manager import IPasswordManager


class PasswordManager(IPasswordManager):
    pwd_context = PasswordHash.recommended()

    def __init__(self, context: CryptContext | None = None):
        if context:
            self.pwd_context = context

    async def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    async def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)





@pytest.mark.django_db
class AuthApiTest(APITestCase):

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        cache.clear() # Очищаем кэш между тестами
        self.creator = UserCreator()
        self.candidate = self.creator.create_user(UserRole.CANDIDATE)

    def _post_register(self, data: dict) -> Response:
        view = AuthApi.as_view({"post": "register"}, permission_classes=[AllowAny])
        request = self.factory.post(
            path="/api/core/auth/register",
            data=data,
            format="json")
        return view(request=request)

    def test_user_create_with_exist_email(self) -> None:
        """Тест регистрации пользователя с уже существующим email."""
        existing_email = user_with_exist_email_data["email"]
        user_in_db = self.candidate
        user_in_db.email = existing_email
        user_in_db.save()

        response = self._post_register(data=user_with_exist_email_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data