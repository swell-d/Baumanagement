from datetime import datetime
from pathlib import Path

from django.contrib.auth.models import User, Group
from django.test import TestCase, Client

from Baumanagement.models.models_comments import Comment
from Baumanagement.models.models_company import CompanyRole, Company, Account, Contact
from Baumanagement.models.models_contracts import Contract, Payment, Bill, ContractTag
from Baumanagement.models.models_files import File
from Baumanagement.models.models_messages import MyMessage
from Baumanagement.models.models_products import Product, ProductCategory
from Baumanagement.models.models_projects import Project, ProjectTag
from Baumanagement.urls import get_urls


class UrlTests(TestCase):
    def setUp(self):
        group = Group.objects.create(name="admins")
        group.save()
        user = User.objects.create(username='test')
        user.set_password('test')
        user.save()

        self.ProductCategory = ProductCategory.objects.create(name='test')
        self.Product = Product.objects.create(name='test')

        self.CompanyRole = CompanyRole.objects.create(name='test')
        self.Company = Company.objects.create(name='test')
        self.Company.role.add(self.CompanyRole)
        self.Company.save()
        self.Account = Account.objects.create(name='test', company=self.Company)
        self.Contact = Contact.objects.create(name='test', company=self.Company)

        self.ProjectTag = ProjectTag.objects.create(name='test')
        self.Project = Project.objects.create(name='test', company=self.Company, tag=self.ProjectTag)

        self.ContractTag = ContractTag.objects.create(name='test')
        self.Contract = Contract.objects.create(name='test', project=self.Project, company=self.Company,
                                                amount_netto_positiv=1, vat=1, date=datetime.now(),
                                                type=Contract.BUY, tag=self.ContractTag)

        self.Payment = Payment.objects.create(name='test', contract=self.Contract, amount_netto_positiv=1, vat=1,
                                              date=datetime.now(),
                                              account_from=self.Account, account_to=self.Account)
        self.Bill = Bill.objects.create(name='test', contract=self.Contract, amount_netto_positiv=1, vat=1,
                                        date=datetime.now())
        self.Comment = Comment.objects.create(name='test')

        self.Message = MyMessage.objects.create(name='test', level=25)

        Path("files").mkdir(parents=True, exist_ok=True)
        with open('files/test.txt', 'w') as file:
            file.write('')
        self.File = File.objects.create(name='test', file='test.txt')

    def test_pages(self):
        client = Client()
        response = client.get('http://127.0.0.1:8000/', follow=True)
        self.assertEqual(response.status_code, 200)

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
                if '/de/' not in url:
                    continue
                response = client.post(url)
                self.assertEqual(response.status_code, 200)
