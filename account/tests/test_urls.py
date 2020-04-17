from django.test import SimpleTestCase
from django.urls import resolve,reverse
from account.views import *

class TestUrls(SimpleTestCase):

    def test_dash_url_resolves(self):
        url = reverse('dash')
        self.assertEquals(resolve(url).func,dash)

    def test_upload_url_resolves(self):
        url = reverse('upload')
        self.assertEquals(resolve(url).func,upload)

    def test_download_url_resolves(self):
        url = reverse('download')
        self.assertEquals(resolve(url).func, download)
    
    def test_account_url_resolves(self):
        url = reverse('account')
        self.assertEquals(resolve(url).func, account)
    
    def test_edituser_url_resolves(self):
        url = reverse('edituser')
        self.assertEquals(resolve(url).func, edituser)

    def test_changepass_url_resolves(self):
        url = reverse('changepass')
        self.assertEquals(resolve(url).func,changepass)
    
    def test_view_url_resolves(self):
        url = reverse('view')
        self.assertEquals(resolve(url).func,view)

    def test_generate_url_resolves(self):
        url = reverse('generate')
        self.assertEquals(resolve(url).func, generate)
    
    def test_upload_file_url_resolves(self):
        url = reverse('upload_file')
        self.assertEquals(resolve(url).func, upload_file)

    def test_download_file_url_resolves(self):
        url = reverse('download_file')
        self.assertEquals(resolve(url).func, download_file)

    def test_delete_file_url_resolves(self):
        url = reverse('delete_file')
        self.assertEquals(resolve(url).func, delete_file)

    def test_delete_account_url_resolves(self):
        url = reverse('delete_account')
        self.assertEquals(resolve(url).func, delete_account)
