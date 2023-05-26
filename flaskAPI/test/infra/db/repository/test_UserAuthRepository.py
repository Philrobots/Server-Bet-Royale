# import unittest

# from main.infra.exception.NonExistingEmailException import NonExistingEmailException
# from test.infra.builder.UserAuthBuilder import UserAuthBuilder

# from main.domain.identifiers.DomainId import DomainId
# from main.infra.db.repository.UserAuthRepository import UserAuthRepository
# from main.infra.exception.NonExistingUserException import \
#     NonExistingUserException

# class UserAuthRepositoryTest(unittest.TestCase):

#     def setUp(self):
#         self.A_USER_ID = DomainId()
#         self.A_USERNAME = "salut1234"
#         self.A_EMAIL = "sauce@sauce.com"
#         self.A_USER_AUTH = UserAuthBuilder().with_username(self.A_USERNAME).with_email(self.A_EMAIL).build()
#         self.repository = UserAuthRepository(self.dao)

#     def test_whenAddUser_thenReturnValidUserId(self):
#         user_id = self.repository.add_user(self.A_USER_AUTH)
#         self.assertEqual(self.A_USER_AUTH.user_id, user_id)

#     def test_givenUserInRepository_whenGetById_thenReturnCorrectUser(self):
#         user_id = self.repository.add_user(self.A_USER_AUTH)

#         actual_user = self.repository.get_by_id(user_id)

#         self.assertEqual(self.A_USER_AUTH, actual_user)

#     def test_givenNoUserdWithGivenId_whenGetById_thenRaiseNonExistingUserException(self):
#         with self.assertRaises(NonExistingUserException):
#             self.repository.get_by_id(self.A_USER_ID)

#     def test_whenGetByUsername_thenReturnCorrectUser(self):
#         self.repository.add_user(self.A_USER_AUTH)

#         actual_user = self.repository.get_by_username(self.A_USERNAME)

#         self.assertEqual(self.A_USER_AUTH, actual_user)

#     def test_whenGetByEmail_thenReturnCorrectUser(self):
#         self.repository.add_user(self.A_USER_AUTH)

#         actual_user = self.repository.get_by_email(self.A_EMAIL)

#         self.assertEqual(self.A_USER_AUTH, actual_user)

#     def test_givenNoUserWithGivenUsername_whenGetByUsername_thenRaiseNonExistingUserException(self):
#         with self.assertRaises(NonExistingUserException):
#             self.repository.get_by_id(self.A_USERNAME)

#     def test_givenNoUserWithGivenEmail_whenGetByEmail_thenRaiseNonExistingEmailException(self):
#         with self.assertRaises(NonExistingEmailException):
#             self.repository.get_by_email(self.A_EMAIL)
