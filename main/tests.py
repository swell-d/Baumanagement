from datetime import datetime
from pathlib import Path

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from APP.urls import get_urls
from bank_accounts.models import Account
from bills.models import Bill
from comments.models import Comment
from companies.models import Company
from companies.models_labels import CompanyLabel
from contacts.models import Contact
from contracts.models import Contract
from contracts.models_labels import ContractLabel
from files.models import File
from notifications.models import Notification
from payments.models import Payment
from products.models import Product
from products.models_labels import ProductCategory
from projects.models import Project
from projects.models_labels import ProjectLabel


class UrlTests(TestCase):
    def setUp(self):
        group = Group.objects.create(name="admins")
        group.save()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        self.ProductCategory = ProductCategory.objects.create(name='test')
        self.Product = Product.objects.create(name='test')
        self.Product.categories.set([self.ProductCategory, ])
        self.Product.save()

        self.CompanyLabel = CompanyLabel.objects.create(name='test')
        self.Company = Company.objects.create(name='test')
        self.Company.label.add(self.CompanyLabel)
        self.Company.save()
        self.Account = Account.objects.create(name='test', company=self.Company)
        self.Contact = Contact.objects.create(name='test', company=self.Company)

        self.ProjectLabel = ProjectLabel.objects.create(name='test')
        self.Project = Project.objects.create(name='test', company=self.Company)
        self.Project.label.add(self.ProjectLabel)
        self.Project.save()

        self.ContractLabel = ContractLabel.objects.create(name='test')
        self.Contract = Contract.objects.create(name='test', project=self.Project, company=self.Company,
                                                amount_netto_positiv=1, vat=1, date=datetime.now(),
                                                type=Contract.BUY)
        self.Contract.label.add(self.ContractLabel)
        self.Contract.save()

        self.Payment = Payment.objects.create(name='test', contract=self.Contract, amount_netto_positiv=1, vat=1,
                                              date=datetime.now(),
                                              account_from=self.Account, account_to=self.Account)
        self.Bill = Bill.objects.create(name='test', contract=self.Contract, amount_netto_positiv=1, vat=1,
                                        date=datetime.now())
        self.Comment = Comment.objects.create(name='test')

        self.Message = Notification.objects.create(name='test', level=25)

        Path("media").mkdir(parents=True, exist_ok=True)
        with open('media/test.txt', 'w') as file:
            file.write('')
        self.File = File.objects.create(name='test', file='test.txt')

    def test_pages(self):
        client = Client()

        client.login(username='test', password='test')

        for url in get_urls():
            print(f'http://127.0.0.1:8000{url}')

            if 'delete' not in url:
                response = client.get(url, follow=True)
                self.assertEqual(response.status_code, 200)
                print(f'http://127.0.0.1:8000{url}?search=1')
                response = client.get(f'{url}?search=1', follow=True)
                self.assertEqual(response.status_code, 200)
            else:
                response = client.post(url)
                self.assertEqual(response.status_code, 200)
