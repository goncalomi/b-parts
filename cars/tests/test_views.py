from django.urls import reverse
from django.test import TestCase, Client

from cars.models import Customer, LicensePlate


class CustomerUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('add_plate')
        self.customer = Customer.objects.create(email='existing@example.com')
        self.plate1 = LicensePlate.objects.create(customer=self.customer, plate_number='00AA00')
        self.plate2 = LicensePlate.objects.create(customer=self.customer, plate_number='00-00-AA')
        self.edit_url = reverse('edit_customer', kwargs={'pk': self.customer.pk})

    def test_new_customer_and_new_license_plate(self):
        response = self.client.post(self.create_url, {
            'email': 'new@example.com',
            'plates-TOTAL_FORMS': '1',
            'plates-INITIAL_FORMS': '0',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-plate_number': '11BB11',
        })
        self.assertTrue(Customer.objects.filter(email='new@example.com').exists())
        self.assertTrue(LicensePlate.objects.filter(plate_number='11BB11').exists())

    def test_invalid_license_plate(self):
        response = self.client.post(self.create_url, {
            'email': 'existing@example.com',
            'plates-TOTAL_FORMS': '1',
            'plates-INITIAL_FORMS': '0',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-plate_number': 'INVALID',
        })
        self.assertFalse(LicensePlate.objects.filter(plate_number='INVALID').exists())

    def test_existing_license_plate(self):
        response = self.client.post(self.create_url, {
            'email': 'new3@example.com',
            'plates-TOTAL_FORMS': '1',
            'plates-INITIAL_FORMS': '0',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-plate_number': '00AA00',
        })
        self.assertEqual(LicensePlate.objects.filter(customer__email='new3@example.com', plate_number='00AA00').count(), 0)

    def test_delete_license_plate(self):
        formset_data = {
            'email': self.customer.email,
            'plates-TOTAL_FORMS': '2',
            'plates-INITIAL_FORMS': '2',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-id': self.plate1.id,
            'plates-0-plate_number': '00AA00',
            'plates-0-DELETE': 'on',
            'plates-1-id': self.plate2.id,
            'plates-1-plate_number': '00-00-AA',
        }
        response = self.client.post(self.edit_url, data=formset_data)
        self.assertFalse(LicensePlate.objects.filter(id=self.plate1.id).exists())
        self.assertTrue(LicensePlate.objects.filter(id=self.plate2.id).exists())


class CustomerListViewTest(TestCase):
    def setUp(self):
        self.customer1 = Customer.objects.create(email='test1@example.com')
        self.customer2 = Customer.objects.create(email='test2@example.com')
        LicensePlate.objects.create(customer=self.customer1, plate_number='00AA00')
        LicensePlate.objects.create(customer=self.customer2, plate_number='00-00-AA')

    def test_list_customers_and_license_plates(self):
        response = self.client.get(reverse('list_plates'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test1@example.com')
        self.assertContains(response, 'test2@example.com')
        self.assertContains(response, '00AA00')
        self.assertContains(response, '00-00-AA')
