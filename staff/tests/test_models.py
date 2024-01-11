from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from staff.models import CafeInfo,staff_user, Staff, OTPCODE, SingletonModel
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

class CafeInfoModelTest(TestCase):
    def setUp(self):
        # Create a sample CafeInfo instance with valid data
        self.cafe = CafeInfo.objects.create(
            coffe_name="Test Cafe",
            phone="1234567890",
            address="Test Address",
            logo=SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        )

    def test_cafe_info_model_fields(self):
        # Test if the model fields are correctly defined
        self.assertEqual(self.cafe.coffe_name, "Test Cafe")
        self.assertEqual(self.cafe.phone, "1234567890")
        self.assertEqual(self.cafe.address, "Test Address")

        # Assuming you are using ImageField, you can check if the logo is not empty
        self.assertIsNotNone(self.cafe.logo)

    # def test_cafe_info_model_str_method(self):
    #     # Test the __str__ method of the model
    #     self.assertEqual(str(self.cafe), "Test Cafe")

   

# Run the tests using the following command:
# python manage.py test your_app --verbosity=2
class UserModelTest(TestCase):
    def setUp(self):
        # Create a sample user instance with valid data
        self.user = get_user_model().objects.create_user(
            email="test@example.com",
            phone_number="1234567890",
            full_name="Test User",
            roll="Test Role",
            password="password123"
        )

    def test_user_model_fields(self):
        # Test if the model fields are correctly defined
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.phone_number, "1234567890")
        self.assertEqual(self.user.full_name, "Test User")
        self.assertEqual(self.user.roll, "Test Role")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

    def test_user_model_str_method(self):
        # Test the __str__ method of the model
        self.assertEqual(str(self.user), "test@example.com")

    def test_user_manager_create_user(self):
        # Test the create_user method of the custom manager
        user = get_user_model().objects.create_user(
            email="test2@example.com",
            phone_number="9876543210",
            full_name="Test User 2",
            roll="Test Role 2",
            password="password456"
        )
        self.assertEqual(user.email, "test2@example.com")
        self.assertEqual(user.phone_number, "9876543210")
        self.assertEqual(user.full_name, "Test User 2")
        self.assertEqual(user.roll, "Test Role 2")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)

    def test_user_manager_create_superuser(self):
        # Test the create_superuser method of the custom manager
        admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            phone_number="9999999999",
            full_name="Admin User",
            roll="Admin Role",
            password="adminpassword"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertEqual(admin_user.phone_number, "9999999999")
        self.assertEqual(admin_user.full_name, "Admin User")
        self.assertEqual(admin_user.roll, "Admin Role")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_admin)



class StaffUserModelTest(TestCase):
    def setUp(self):
        # Create a sample staff_user instance with valid data
        self.staff_user = staff_user.objects.create(
            name="Test Staff User",
            email="test_staff@example.com",
            phone_number="1234567890"
        )

    def test_staff_user_model_fields(self):
        # Test if the model fields are correctly defined
        self.assertEqual(self.staff_user.name, "Test Staff User")
        self.assertEqual(self.staff_user.email, "test_staff@example.com")
        self.assertEqual(self.staff_user.phone_number, "1234567890")

    # def test_staff_user_str_method(self):
    #     # Test the __str__ method of the staff_user model
    #     self.assertEqual(str(self.staff_user), "Test Staff User")
        
class StaffModelTest(TestCase):
    def setUp(self):
        # Create a sample Staff instance with valid data
        self.staff_member = Staff.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="1234567890"
        )

    def test_staff_model_fields(self):
        # Test if the model fields are correctly defined
        self.assertEqual(self.staff_member.first_name, "John")
        self.assertEqual(self.staff_member.last_name, "Doe")
        self.assertEqual(self.staff_member.phone_number, "1234567890")

    def test_staff_model_str_method(self):
        # Test the __str__ method of the Staff model
        self.assertEqual(str(self.staff_member), "John Doe")

    def test_staff_model_unique_phone_number(self):
        # Test that the phone_number field is unique
        with self.assertRaises(Exception):
            Staff.objects.create(
                first_name="Jane",
                last_name="Doe",
                phone_number="1234567890"  # This phone number should raise a unique constraint error
            )


class OTPCODEModelTest(TestCase):
    def setUp(self):
        # Create a sample OTPCODE instance with valid data
        self.otp_code = OTPCODE.objects.create(
            phone_number="1234567890",
            code=1234,
            created=datetime.now() - timedelta(days=1)
        )

    # def test_otpcodes_model_fields(self):
    #     # Test if the model fields are correctly defined
    #     self.assertEqual(self.otp_code.phone_number, "1234567890")
    #     self.assertEqual(self.otp_code.code, 1234)
    #     self.assertLess(self.otp_code.created, datetime.now())  # Ensure created is in the past

    # def test_otpcodes_model_str_method(self):
    #     # Test the __str__ method of the OTPCODE model
    #     self.assertEqual(
    #         str(self.otp_code),
    #         f"1234567890 - 1234 - {self.otp_code.created.strftime('%Y-%m-%d %H:%M:%S')}"
    #     )

    # def test_otpcodes_model_recent_created(self):
    #     # Test that the created field is recent
    #     recent_otp = OTPCODE.objects.create(
    #         phone_number="9876543210",
    #         code=5678,
    #         created=datetime.now()
    #     )
    #     self.assertGreater(recent_otp.created, datetime.now() - timedelta(minutes=1))
        

class SingletonModelTest(TestCase):
    # def setUp(self):
    #     # Create a sample SingletonModel instance
    #     self.singleton_instance = SingletonModel()

    # def test_singleton_model_load(self):
    #     # Test the load method of the SingletonModel
    #     loaded_instance = SingletonModel.load()
    #     self.assertIsNone(loaded_instance)  # Since there's no instance created yet

        # Save the instance and test again
        # self.singleton_instance.save()
        # loaded_instance = SingletonModel.load()
        # self.assertIsNotNone(loaded_instance)
        # self.assertEqual(loaded_instance.pk, 1)

    # def test_singleton_model_save(self):
    #     # Test the save method of the SingletonModel
    #     self.singleton_instance.save()
    #     loaded_instance = SingletonModel.load()
    #     self.assertIsNotNone(loaded_instance)
    #     self.assertEqual(loaded_instance.pk, 1)

    # def test_singleton_model_delete(self):
    #     # Test the delete method of the SingletonModel
    #     with self.assertRaises(NotImplementedError):
    #         self.singleton_instance.delete()

    def test_singleton_model_abstract(self):
        # Test that the SingletonModel is abstract
        self.assertTrue(SingletonModel._meta.abstract)
