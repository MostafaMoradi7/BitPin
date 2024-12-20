from locust import HttpUser, task, between
from faker import Faker
import random
import string

fake = Faker()


class ContentUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def add_content(self):
        content_data = {
            "title": fake.sentence(),
            "description": fake.text(),
        }

        response = self.client.post("/api/contents/", json=content_data)

        if response.status_code == 201:
            print(f"Content added successfully: {content_data['title']}")
        else:
            print(f"Failed to add content: {content_data['title']}")

    @task(2)
    def add_bulk_contents(self):
        for i in range(100):
            content_data = {
                "title": fake.sentence(),
                "description": fake.text(),
            }
            response = self.client.post("/api/contents/", json=content_data)
            if response.status_code != 201:
                print(f"Failed to add content: {content_data['title']}")


class UserCreationTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_user(self):
        user_data = {
            "username": self.generate_username(),
            "email": fake.email(),
            "password": self.generate_password(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
        }

        self.client.post("/api/register/", json=user_data)

    def generate_username(self):
        """Generate a random username"""
        return fake.user_name() + str(random.randint(1000, 9999))

    def generate_password(self):
        """Generate a random password"""
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))


class UserVotingTest(HttpUser):
    wait_time = between(1, 3)
    users = []
    items = {}

    def on_start(self):
        """Called when a simulated user starts."""
        if not self.users:
            with open("users-sample.txt", "r") as file:
                self.users = [line.strip().split(",") for line in file.readlines()]
        self.username, self.email = random.choice(self.users)
        self.password = (
            "1234"  # I've manually set the password of all test users to this
        )
        response = self.client.post(
            "/api/auth/", json={"username": self.username, "password": self.password}
        )
        if response.status_code == 200:
            token = response.json().get("access")

            self.items["token"] = token

            self.items["headers"] = {"Authorization": f"Bearer {token}"}

        else:
            print(f"Failed to login for user {self.username}")

    @task
    def vote(self):
        """Simulate a user voting on content."""
        content_id = self.get_content_ids()
        score = random.randint(0, 5)

        vote_data = {"content": content_id, "score": score}

        response = self.client.post(
            "/api/vote/",
            json=vote_data,
            headers=self.items.get("headers"),
        )

        if response.status_code == 201:
            print(
                f"User {self.username} voted on content {content_id} with score {score}"
            )
        elif response.status_code == 200:
            print(
                f"User {self.username} updated vote for content {content_id} to score {score}"
            )
        else:
            print(f"Error: {response.status_code} - {response.text}")

    def get_content_ids(self):
        """Fetch a random content ID."""
        return random.randint(0, 3000)  # 3000 sample content created in db
        # return 1112  # attacking to one content
