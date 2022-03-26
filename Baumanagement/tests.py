from datetime import datetime

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from Baumanagement.models import CompanyRole, Company, Project, Contract, Payment, Bill, File
from Baumanagement.urls import get_urls


class UrlTests(TestCase):
    def setUp(self):
        self.CompanyRole = CompanyRole.objects.create(name='test')
        self.Company = Company.objects.create(name='test').role.add(self.CompanyRole)
        self.Project = Project.objects.create(name='test', company_id=1)
        self.Contract = Contract.objects.create(name='test', project_id=1, company_id=1, amount_netto=1, vat=1,
                                                amount_brutto=1, date=datetime.now())
        self.Payment = Payment.objects.create(name='test', contract_id=1, amount_netto=1, vat=1, amount_brutto=1,
                                              date=datetime.now())
        self.Bill = Bill.objects.create(name='test', contract_id=1, amount_netto=1, vat=1, amount_brutto=1,
                                        date=datetime.now())
        self.File = File.objects.create(name='test', file=b'')

        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        group = Group.objects.create(name="admins")
        group.save()

    def test_pages(self):
        client = Client()
        logged_in = client.login(username='test', password='test')

        for url in get_urls():
            print(f'http://127.0.0.1:8000{url}')
            response = client.get(url)
            if 'delete' not in url:
                self.assertEqual(response.status_code, 200)
                print(f'http://127.0.0.1:8000{url}?search=')
                response = client.get(f'{url}?search=')
                self.assertEqual(response.status_code, 200)
            else:
                self.assertEqual(response.status_code, 302)
