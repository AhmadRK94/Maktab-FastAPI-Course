from locust import HttpUser, task, between
from requests.cookies import create_cookie


class LoadTestingExpenses(HttpUser):
    wait_time = between(0.1, 1)

    def on_start(self):
        response = self.client.post(
            "/auth/login", json={"email": "ahmad@gmail.com", "password": "a123456"}
        )

        access_token = response.cookies.get("access_token")
        refresh_token = response.cookies.get("refresh_token")

        if access_token:
            cookie = create_cookie(name="access_token", value=access_token)
            self.client.cookies.set_cookie(cookie)
        if refresh_token:
            cookie = create_cookie(name="refresh_token", value=refresh_token)
            self.client.cookies.set_cookie(cookie)

    @task(2)
    def get_all_users(self):
        self.client.get("/users")

    @task
    def get_authorized_user_expenses(self):
        self.client.get("/expenses")
