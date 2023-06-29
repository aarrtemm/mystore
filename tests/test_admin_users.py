from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'media/products_images/images.jpg',
            content_type='image/jpeg'
        )
        self.admin = get_user_model().objects.create_superuser(
            "admin",
            "12345678fgh"
        )
        self.client.force_login(self.admin)

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            image=image_file
        )

    def test_user_change_image_listed(self):
        url = reverse("admin:users_user_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertContains(response, self.user.image)

    def test_user_add_image_listed(self):
        url = reverse("admin:users_user_add")

        response = self.client.get(url)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "Image")
