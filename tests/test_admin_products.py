from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UserAdminTestCase(TestCase):
    def setUp(self):
        self.admin_username = "admin"
        self.admin_password = "admin123"
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username=self.admin_username, password=self.admin_password
        )

    def test_user_admin_additional_info_fields(self):
        self.client.login(username=self.admin_username, password=self.admin_password)

        change_url = reverse("admin:users_user_change", args=(self.user.pk,))

        response = self.client.get(change_url)

        self.assertContains(response, "id_image")

    def test_user_admin_additional_info_fields_in_add_form(self):
        # Login as admin
        self.client.login(username=self.admin_username, password=self.admin_password)

        add_url = reverse("admin:users_user_add")

        response = self.client.get(add_url)

        self.assertContains(response, "id_first_name")
        self.assertContains(response, "id_last_name")
        self.assertContains(response, "id_image")
