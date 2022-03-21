from datetime import datetime

from django.test import TestCase, Client

from Baumanagement.models import CompanyRole, Company, Project, Contract, Payment, Bill
from Baumanagement.urls import get_urls


class UrlTests(TestCase):
    def setUp(self):
        self.CompanyRole = CompanyRole.objects.create(name='test')
        self.Company = Company.objects.create(name='test')
        self.Project = Project.objects.create(name='test', company_id=1)
        self.Contract = Contract.objects.create(name='test', project_id=1, company_id=1, amount=1, date=datetime.now())
        self.Payment = Payment.objects.create(name='test', contract_id=1, amount=1, date=datetime.now())
        self.Bill = Bill.objects.create(name='test', contract_id=1, amount=1, date=datetime.now())

    def test_pages(self):
        client = Client()
        for url in get_urls():
            response = client.get(url)
            self.assertEqual(response.status_code, 200)
