from django.test import TestCase, Client
from django.urls import reverse, resolve
from .models import Account, User
from .views import register_account, read_akun, update_akun
import environ

env = environ.Env()
environ.Env.read_env()

REVERSE_ACC_REGIST = 'account:registerAccount'
REGIST_HTML = 'register_account.html'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_ADMIN_EMAIL = 'test.admin@gmail.com'
TEST_ADMIN_PASSWORD = 'testadmin123'
TEST_USER_USERNAME = 'test_user'
TEST_USER_EMAIL = 'test.user@gmail.com'
TEST_USER_PASSWORD = 'testuser123'
TEST_SK_EMAIL = 'test.sk@gmail.com'

ACCOUNT_URL = '/account/'
GANTI_STATUS_AKUN_URL = '/account/ganti-status-akun'
UNEXPECTED_HTML = 'unexpected.html'
PASSWORD_UNTUK_TEST = env('PASSWORD_UNTUK_TEST')

def create_test_users():
    '''Create test users and accounts'''
    admin_user = User.objects.create(username='test_admin', email=TEST_ADMIN_EMAIL)
    admin_user.set_password('testadmin123')
    admin_user.save()
    Account.objects.create(user=admin_user, username='test_admin', email=TEST_ADMIN_EMAIL, role='Admin')

    user_user = User.objects.create(username='test_user', email=TEST_USER_EMAIL)
    user_user.set_password('testuser123')
    user_user.save()
    Account.objects.create(user=user_user, username='test_user', email=TEST_USER_EMAIL, role='User')

    sk_user = User.objects.create(username='test_sk', email=TEST_SK_EMAIL)
    sk_user.set_password('testsk123')
    sk_user.save()
    Account.objects.create(user=sk_user, username='test_sk', email=TEST_SK_EMAIL, role='Staff Keuangan')


class ModelTest(TestCase):
    '''Test Module for models'''

    def setUp(self):
        '''Create object to test based on models'''
        create_test_users()

    def test_model_user_return_str(self):

        user_admin = User.objects.get(username='test_admin')
        self.assertEqual(user_admin.username,'test_admin')
        self.assertEqual(user_admin.email,TEST_ADMIN_EMAIL)
        
        user_user = User.objects.get(username='test_user')
        self.assertEqual(user_user.username,'test_user')
        self.assertEqual(user_user.email,TEST_USER_EMAIL)
        
        user_sk = User.objects.get(username='test_sk')
        self.assertEqual(user_sk.username,'test_sk')
        self.assertEqual(user_sk.email,TEST_SK_EMAIL)

    def test_model_account_return_str(self):

        admin_acc = User.objects.get(username='test_admin')
        self.assertEqual(admin_acc.username,'test_admin')
        self.assertEqual(admin_acc.email, TEST_ADMIN_EMAIL)
        
        user_acc = User.objects.get(username='test_user')
        self.assertEqual(user_acc.username,'test_user')
        self.assertEqual(user_acc.email,TEST_USER_EMAIL)
        
        sk_acc = User.objects.get(username='test_sk')
        self.assertEqual(sk_acc.username,'test_sk')
        self.assertEqual(sk_acc.email,TEST_SK_EMAIL)

class RegisterAccountViewTest(TestCase):
    '''Test Module for Register Account'''

    def setUp(self):
        '''Create object to test based on models'''
        create_test_users()

        self.form_data_user = {
            'username': 'testuser',
            'email': 'testuser@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'User',
        }

        self.form_data_admin = {
            'username': 'testadmin',
            'email': 'testadmin@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'role': 'Admin',
        }

        self.form_invalid = {
            'username': TEST_ADMIN_USERNAME,
            'email': 'testadmin@test.com',
            'password1': 'testpassword',
            'password2': 'testpassword1',
            'role': 'Admin',
        }

    def test_register_account_user_view_with_authenticated_admin_user(self):
        self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
        url = reverse(REVERSE_ACC_REGIST)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, REGIST_HTML)

        # submit valid form data
        response = self.client.post(url, data=self.form_data_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Account.objects.all()), 4) # check if account was created
        self.assertTrue(User.objects.filter(username='testuser').exists()) # check if user was created
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_staff)

    def test_register_account_admin_view_with_authenticated_admin_user(self):
        self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
        url = reverse(REVERSE_ACC_REGIST)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, REGIST_HTML)

        # submit valid form data
        response = self.client.post(url, data=self.form_data_admin)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Account.objects.all()), 4) # check if account was created
        self.assertTrue(User.objects.filter(username='testadmin').exists()) # check if user was created
        user = User.objects.get(username='testadmin')
        self.assertTrue(user.is_staff)
        

    def test_register_account_view_with_unauthenticated_user(self):
        url = reverse(REVERSE_ACC_REGIST)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/account/register')
        response = self.client.post(url, data=self.form_data_user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login?next=/account/register')

    def test_register_account_view_with_authenticated_non_admin_user(self):
        self.client.login(username=TEST_USER_USERNAME, password=TEST_USER_PASSWORD)
        url = reverse(REVERSE_ACC_REGIST)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
    
    def test_register_account_view_with_non_unique_username(self):
        self.client.login(username=TEST_ADMIN_USERNAME, password=TEST_ADMIN_PASSWORD)
        url = reverse(REVERSE_ACC_REGIST)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, REGIST_HTML)

        # submit invalid form data
        response = self.client.post(url, data=self.form_invalid)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Account.objects.all()), 3) # check if account was created
        self.assertFalse(User.objects.filter(username='testuser').exists()) # check if user was created


def set_up_login(self, role):
    self.client = Client()
    USERNAME = 'tesname'
    PASSWORD = PASSWORD_UNTUK_TEST
    user: User = User.objects.create()
    user.username = USERNAME
    user.set_password(PASSWORD)
    account = Account(
        user = user,
        username = USERNAME, 
        email = 'tes@gmail.com',
        role = role
    )
    account.user.username=USERNAME
    user.save()
    account.save()

    login = self.client.login(username=USERNAME, password=PASSWORD)
    self.assertTrue(login)

def set_up_akun_dummy(self):
    self.USERNAME = 'tesname2'
    self.PASSWORD = PASSWORD_UNTUK_TEST
    self.EMAIL = 'tes@gmail.com'
    user: User = User.objects.create()
    user.username = self.USERNAME
    user.set_password(self.PASSWORD)
    account = Account(
        user = user,
        username = self.USERNAME, 
        email = self.EMAIL,
        role = 'Admin'
    )
    account.user.username = self.USERNAME
    user.save()
    account.save()

    self.user_dummy = user
    self.account_dummy = account

class AccountTidakLoginTest(TestCase):
    def test_read_akun_is_exist(self):
        response = Client().get(ACCOUNT_URL)
        # karena belum login, diarahkan ke halaman login
        self.assertRedirects(response, f'/login?next=/account/', status_code=302, target_status_code=200)

    def test_using_read_akun_func(self):
        found = resolve(ACCOUNT_URL)
        self.assertEqual(found.func, read_akun)

    def test_update_akun_is_exist(self):
        response = Client().get('/account/update/1')
        # karena belum login, diarahkan ke halaman login
        self.assertRedirects(response, f'/login?next=/account/update/1', status_code=302, target_status_code=200)

    def test_using_update_akun_func(self):
        found = resolve('/account/update/1')
        self.assertEqual(found.func, update_akun)

    def test_ganti_status_akun_is_exist(self):
        response = Client().post(GANTI_STATUS_AKUN_URL)
        # karena belum login, diarahkan ke halaman login
        self.assertRedirects(response, f'/login?next=/account/ganti-status-akun', status_code=302, target_status_code=200)



class AccountSudahLoginAdminTest(TestCase):
    def setUp(self) -> None:
        set_up_login(self, 'Admin')
        set_up_akun_dummy(self)

    def test_admin_read_akun_is_exist(self):
        response = self.client.get(ACCOUNT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'read_akun.html')

    def test_admin_update_akun_is_exist(self):
        response = self.client.get(f'/account/update/{self.account_dummy.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_akun.html')
        
    def test_admin_update_akun_id_ngasal(self):
        response = self.client.get(f'/account/update/3333')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_admin_update_akun_id_bukan_int(self):
        response = self.client.get(f'/account/update/aasdd')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_admin_update_akun_post_is_exist(self):
        data = {
            'id_akun': self.account_dummy.id,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertRedirects(response, ACCOUNT_URL, status_code=302, target_status_code=200)
        
        updated_account = Account.objects.get(user=self.user_dummy)
        self.assertEqual(updated_account.role, "User")

    def test_admin_update_akun_post_id_ngasal(self):
        data = {
            'id_akun': 3333,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_admin_update_akun_post_id_bukan_int(self):
        data = {
            'id_akun': 'aassdd',
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_admin_ganti_status_akun_is_exist(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': self.account_dummy.id})
        status_awal = self.user_dummy.is_active
        self.assertRedirects(response, ACCOUNT_URL, status_code=302, target_status_code=200)
        updated_akun = User.objects.get(username=self.USERNAME)
        status_updated = updated_akun.is_active
        self.assertEqual(status_updated, not status_awal)

    def test_admin_ganti_status_akun_id_ngasal(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': 3333})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_admin_ganti_status_akun_id_bukan_int(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': 'aasdd'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)


class AccountSudahLoginUserTest(TestCase):
    def setUp(self) -> None:
        set_up_login(self, 'User')
        set_up_akun_dummy(self)
        

    def test_user_read_akun_is_exist(self):
        response = self.client.get(ACCOUNT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_update_akun_is_exist(self):
        response = self.client.get(f'/account/update/{self.account_dummy.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_update_akun_id_ngasal(self):
        response = self.client.get(f'/account/update/3333')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_update_akun_id_bukan_int(self):
        response = self.client.get(f'/account/update/aasdd')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_update_akun_post_tidak_bisa(self):
        data = {
            'id_akun': self.account_dummy.id,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)
        
        updated_account = Account.objects.get(user=self.user_dummy)
        self.assertEqual(updated_account.role, "Admin") # Tidak terupdate

    def test_user_update_akun_post_id_ngasal(self):
        data = {
            'id_akun': 3333,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_update_akun_id_post_bukan_int(self):
        data = {
            'id_akun': 'aassdd',
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)


    def test_user_ganti_status_akun_is_exist(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': self.account_dummy.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_ganti_status_akun_id_ngasal(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': 3333})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_user_ganti_status_akun_id_bukan_int(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': 'aassdd'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)


class AccountSudahLoginStaffKeuanganTest(TestCase):
    def setUp(self) -> None:
        set_up_login(self, 'Staff Keuangan')
        set_up_akun_dummy(self)


    def test_staff_keuangan_read_akun_is_exist(self):
        response = self.client.get(ACCOUNT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_staff_keuangan_update_akun_is_exist(self):
        data = {
            'id_akun': self.account_dummy.id,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_staff_keuangan_update_akun_id_ngasal(self):
        response = self.client.get(f'/account/update/3333')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_staff_keuangan_update_akun_id_bukan_int(self):
        response = self.client.get(f'/account/update/aasdd')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_staff_keuangan_update_akun_post_tidak_bisa(self):
        data = {
            'id_akun': self.account_dummy.id,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)
        
        updated_account = Account.objects.get(user = self.user_dummy)
        self.assertEqual(updated_account.role, "Admin") # Tidak terupdate

    def test_staff_keuangan_update_akun_post_id_ngasal(self):
        data = {
            'id_akun': 3333,
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_staff_keuangan_update_akun_post_id_bukan_int(self):
        data = {
            'id_akun': 'aassdd',
            'role': "User"
        }
        response = self.client.post(f'/account/update/submit/submit', data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)


    def test_staff_keuangan_ganti_status_akun_is_exist(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': self.account_dummy.id})
        self.assertEqual(response.status_code, 200)

    def test_staff_keuangan_ganti_status_akun_id_ngasal(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': 3333})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)

    def test_staff_keuangan_ganti_status_akun_id_bukan_int(self):
        response = self.client.post(GANTI_STATUS_AKUN_URL, {'id_akun': 'aassdd'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, UNEXPECTED_HTML)