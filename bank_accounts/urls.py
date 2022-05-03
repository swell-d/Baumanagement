from django.urls import path

import Baumanagement.views.views_payments
import bank_accounts.views

urlpatterns = [
    path("accounts", bank_accounts.views.objects_table, name="accounts"),
    path("account/<int:id>", bank_accounts.views.object_table, name="account_id"),
    path("account/<int:id>/payments", Baumanagement.views.views_payments.account_payments, name="account_id_payments")
]
