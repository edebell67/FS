from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from server import create_app


class FakeWaitlistStore:
    def __init__(self) -> None:
        self.saved = []

    async def register(self, registration):
        self.saved.append(registration)
        return False


class WaitlistApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.store = FakeWaitlistStore()
        self.client = TestClient(create_app(waitlist_store=self.store))

    def test_accepts_attributed_consent_registration(self) -> None:
        response = self.client.post(
            "/api/waitlist",
            json={
                "email": "owner@example.com",
                "discoverySource": "x",
                "utmSource": "x",
                "utmCampaign": "agentic-arena-launch",
                "landingPath": "/waitlist/",
                "consent": True,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"status": "registered", "duplicate": False})
        self.assertEqual(len(self.store.saved), 1)
        self.assertEqual(self.store.saved[0].discovery_source, "x")

    def test_rejects_missing_consent_without_writing(self) -> None:
        response = self.client.post(
            "/api/waitlist",
            json={"email": "owner@example.com", "discoverySource": "x", "consent": False},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["detail"], "email consent is required")
        self.assertEqual(self.store.saved, [])

    def test_fails_closed_when_waitlist_storage_is_unavailable(self) -> None:
        response = TestClient(create_app()).post(
            "/api/waitlist",
            json={"email": "owner@example.com", "discoverySource": "x", "consent": True},
        )

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["detail"], "waitlist registration is unavailable")


if __name__ == "__main__":
    unittest.main()
