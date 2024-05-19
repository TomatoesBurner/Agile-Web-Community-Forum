import unittest

#auth
from tests.unittest.auth.test_login import TestLogin
from tests.unittest.auth.test_logout import TestLogout
from tests.unittest.auth.test_register import TestRegister
from tests.unittest.auth.test_security_question import TestSecurityQuestion
from tests.unittest.auth.test_forgot_password import TestForgotPassword
#nofity
from tests.unittest.notify.test_inbox import TestNotifications
#postCom
from tests.unittest.postCom.test_create_comment import TestCreateComment
from tests.unittest.postCom.test_create_post import TestCreatePost
from tests.unittest.postCom.test_accept_comment import TestAcceptComment
from tests.unittest.postCom.test_index import TestIndex
from tests.unittest.postCom.test_post_detail import TestPostDetail
from tests.unittest.postCom.test_search import TestSearch
#profile
from tests.unittest.profile.test_profile_module import ProfileTestCase




def suite():
    test_suite = unittest.TestSuite()


    test_suite.addTests([
        #Auth
        unittest.defaultTestLoader.loadTestsFromTestCase(TestLogin),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestLogout),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRegister),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestSecurityQuestion),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestForgotPassword),
        #notfiy
        unittest.defaultTestLoader.loadTestsFromTestCase(TestNotifications),
        #postCom
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCreateComment),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestPostDetail),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestAcceptComment),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestSearch),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCreatePost),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestIndex),
        # profile
        unittest.defaultTestLoader.loadTestsFromTestCase(ProfileTestCase),
    ])

    return test_suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
