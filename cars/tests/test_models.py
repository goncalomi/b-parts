from django.test import TestCase
from django.core.exceptions import ValidationError

from cars.models import Customer, LicensePlate


class CustomerModelTest(TestCase):
    def test_create_customer_with_correct_email(self):
        customer = Customer.objects.create(email="test@example.com")
        self.assertEqual(customer.email, "test@example.com")

    def test_create_customer_with_bad_email_format(self):
        with self.assertRaises(ValidationError):
            customer = Customer(email="bad-email")
            customer.full_clean()

class LicensePlateModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email="test@example.com")

    def test_create_valid_license_plate_with_user(self):
        license_plate = LicensePlate.objects.create(customer=self.customer, plate_number="00AA00")
        self.assertEqual(license_plate.plate_number, "00AA00")
        self.assertEqual(license_plate.customer, self.customer)

    def test_create_valid_license_plate_without_user(self):
        with self.assertRaises(ValidationError):
            license_plate = LicensePlate(plate_number="00AA00")
            license_plate.full_clean()

    def test_create_bad_license_plate_with_user(self):
        invalid_plates = ["INVALID", "1234", "AABBCC", "00-AA-00", "00aa00", "0000AA"]
        for plate in invalid_plates:
            with self.assertRaises(ValidationError):
                license_plate = LicensePlate(customer=self.customer, plate_number=plate)
                license_plate.full_clean()

    def test_create_existing_license_plate_with_user(self):
        LicensePlate.objects.create(customer=self.customer, plate_number="00AA00")
        with self.assertRaises(ValidationError):
            duplicate_plate = LicensePlate(customer=self.customer, plate_number="00AA00")
            duplicate_plate.full_clean() 