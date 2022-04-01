from datetime import datetime
from pathlib import Path

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from Baumanagement.models.models import Project, Contract, Payment, Bill
from Baumanagement.models.models_comments import Comment
from Baumanagement.models.models_company import CompanyRole, Company, Account, Currency, Contact
from Baumanagement.models.models_files import File
from Baumanagement.urls import get_urls


class UrlTests(TestCase):
    def setUp(self):
        self.CompanyRole = CompanyRole.objects.create(name='test')
        self.Company = Company.objects.create(name='test')
        self.Company.role.add(self.CompanyRole)
        self.Company.save()
        self.Currency = Currency.objects.create(name='test', code='test')
        self.Account = Account.objects.create(name='test', company=self.Company, currency=self.Currency)
        self.Contact = Contact.objects.create(name='test', company=self.Company)
        self.Project = Project.objects.create(name='test', company=self.Company)
        self.Contract = Contract.objects.create(name='test', project=self.Project, company=self.Company,
                                                amount_netto=1, vat=1, amount_brutto=1, date=datetime.now())
        self.Payment = Payment.objects.create(name='test', contract=self.Contract,
                                              amount_netto=1, vat=1, amount_brutto=1, date=datetime.now())
        self.Bill = Bill.objects.create(name='test', contract=self.Contract,
                                        amount_netto=1, vat=1, amount_brutto=1, date=datetime.now())
        self.Comment = Comment.objects.create(name='test')

        Path("files").mkdir(parents=True, exist_ok=True)
        with open('files/test.txt', 'w') as file:
            file.write('')
        self.File = File.objects.create(name='test', file='test.txt')

        self.client.force_login(User.objects.get_or_create(username='testuser')[0])
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()
        group = Group.objects.create(name="admins")
        group.save()

    def test_pages(self):
        client = Client()
        response = client.get('http://127.0.0.1:8000/', follow=True)
        self.assertEqual(response.status_code, 200)

        logged_in = client.login(username='test', password='test')

        for url in get_urls():
            print(f'http://127.0.0.1:8000{url}')

            if 'delete' not in url:
                response = client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                print(f'http://127.0.0.1:8000{url}?search=1')
                response = client.get(f'{url}?search=1', follow=True)
                self.assertEqual(response.status_code, 200)
            else:
                if '/de/' not in url:
                    continue
                response = client.post(url)
                self.assertEqual(response.status_code, 200)
