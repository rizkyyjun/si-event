from django.test import TestCase
from account.tests import set_up_akun_dummy, set_up_login
from django.urls import reverse

URL_HOME = reverse("home:home")
URL_FORBIDDEN = reverse("home:forbidden")


class DisplayNotAuthenticatedTest(TestCase):
    def test_display_home_not_authenticated(self):
        response = self.client.get(URL_HOME)
        # karena belum login, diarahkan ke halaman login
        self.assertRedirects(
            response, f"/login?next=/home/", status_code=302, target_status_code=200
        )

    def test_display_forbidden_not_authenticated(self):
        response = self.client.get(URL_FORBIDDEN)
        # karena belum login, diarahkan ke halaman login
        self.assertRedirects(
            response,
            f"/login?next=/home/forbidden/",
            status_code=302,
            target_status_code=200,
        )


class DisplayTestAdmin(TestCase):
    def setUp(self) -> None:
        set_up_login(self, "Admin")
        set_up_akun_dummy(self)

    def test_display_home_template(self):
        response = self.client.get(URL_HOME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_permissions_to_access_display_forbidden(self):
        response = self.client.get(URL_FORBIDDEN)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forbidden.html")

class DisplayTestGuest(TestCase):
    def setUp(self) -> None:
        set_up_login(self, "Guest")
        set_up_akun_dummy(self)

    def test_guest_display_home_template(self):
        response = self.client.get(URL_HOME)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_guest_permissions_to_access_display_forbidden(self):
        response = self.client.get(URL_FORBIDDEN)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "forbidden.html")
