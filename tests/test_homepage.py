from pages.HomePage import HomePage
from tests.test_base import BaseTest


class TestHomePage(BaseTest):

    def test_verify_version_passed(self):
        self.homepage = HomePage(self.driver)

        assert '2.1.0.11' in self.homepage.get_version()

    def test_verify_version_failed(self):
        self.homepage = HomePage(self.driver)

        assert '2.1.0.50' in self.homepage.get_version()

    # def test_verify_version_broken(self):
    #    raise (RuntimeError("Demo Script Thrown an Exception"))
