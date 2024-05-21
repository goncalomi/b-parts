from django.test import TestCase

from cars.models import Customer, LicensePlate
from cars.forms import CustomerForm, LicensePlateInlineFormSet

class CustomerFormTest(TestCase):
    def test_valid_customer_form(self):
        form = CustomerForm(data={'email': 'test@example.com'})
        self.assertTrue(form.is_valid())

    def test_invalid_customer_form(self):
        form = CustomerForm(data={'email': 'invalid-email'})
        self.assertFalse(form.is_valid())

class LicensePlateFormSetTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email='test@example.com')

    def test_valid_license_plate_inline_formset(self):
        formset_data = {
            'plates-TOTAL_FORMS': '1',
            'plates-INITIAL_FORMS': '0',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-plate_number': '00AA00',
        }
        formset = LicensePlateInlineFormSet(prefix='plates', data=formset_data, instance=self.customer)
        self.assertTrue(formset.is_valid(), msg=formset.get_form_error())

    def test_invalid_license_plate_inline_formset(self):
        invalid_plate_data = [
            {'plates-0-plate_number': 'INVALID'},
            {'plates-0-plate_number': '1234'},
            {'plates-0-plate_number': 'AABBCC'},
            {'plates-0-plate_number': '00-AA-00'},
            {'plates-0-plate_number': '00A00A'},
            {'plates-0-plate_number': '00-00-0A'},
        ]

        for form_data in invalid_plate_data:
            formset_data = {
                'plates-TOTAL_FORMS': '1',
                'plates-INITIAL_FORMS': '0',
                'plates-MIN_NUM_FORMS': '0',
                'plates-MAX_NUM_FORMS': '1000',
            }
            formset_data.update(form_data)

            with self.subTest(form_data=form_data):
                formset = LicensePlateInlineFormSet(prefix='plates', data=formset_data, instance=self.customer)
                self.assertFalse(formset.is_valid())
                self.assertIn('plate_number', formset.errors[0])

    def test_create_valid_license_plate(self):
        formset_data = {
            'plates-TOTAL_FORMS': '1',
            'plates-INITIAL_FORMS': '0',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-plate_number': '00AA00',
        }
        formset = LicensePlateInlineFormSet(prefix='plates', data=formset_data, instance=self.customer)
        if formset.is_valid():
            formset.save()
        self.assertEqual(LicensePlate.objects.count(), 1)

    def test_create_invalid_license_plate(self):
        formset_data = {
            'plates-TOTAL_FORMS': '1',
            'plates-INITIAL_FORMS': '0',
            'plates-MIN_NUM_FORMS': '0',
            'plates-MAX_NUM_FORMS': '1000',
            'plates-0-plate_number': 'INVALID',
        }
        formset = LicensePlateInlineFormSet(prefix='plates', data=formset_data, instance=self.customer)
        self.assertFalse(formset.is_valid())
        self.assertEqual(LicensePlate.objects.count(), 0)

    def tearDown(self) -> None:
        return super().tearDown()