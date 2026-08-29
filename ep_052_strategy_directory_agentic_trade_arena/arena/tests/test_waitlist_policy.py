from __future__ import annotations

import unittest

from waitlist_policy import ValidationError, normalize_registration


class WaitlistPolicyTests(unittest.TestCase):
    def test_normalizes_explicit_and_campaign_lead_source(self) -> None:
        registration = normalize_registration(
            {
                "email": "  ELLA@Example.COM ",
                "discoverySource": "x",
                "sourceDetail": "Saw the Arena launch cut",
                "utmSource": "x",
                "utmMedium": "organic_social",
                "utmCampaign": "agentic-arena-launch",
                "landingPath": "/waitlist/",
                "referrer": "https://x.com/thetechprinciple/status/123",
                "consent": True,
            }
        )

        self.assertEqual(registration.email, "ella@example.com")
        self.assertEqual(registration.discovery_source, "x")
        self.assertEqual(registration.source_detail, "Saw the Arena launch cut")
        self.assertEqual(registration.utm_source, "x")
        self.assertEqual(registration.utm_medium, "organic_social")
        self.assertEqual(registration.utm_campaign, "agentic-arena-launch")
        self.assertEqual(registration.landing_path, "/waitlist/")
        self.assertEqual(registration.referrer, "https://x.com/thetechprinciple/status/123")

    def test_rejects_registration_without_email_consent(self) -> None:
        with self.assertRaisesRegex(ValidationError, "consent"):
            normalize_registration(
                {"email": "ella@example.com", "discoverySource": "x", "consent": False}
            )

    def test_rejects_invalid_email_and_honeypot_submission(self) -> None:
        with self.assertRaisesRegex(ValidationError, "email"):
            normalize_registration(
                {"email": "not-an-email", "discoverySource": "x", "consent": True}
            )

        with self.assertRaisesRegex(ValidationError, "submission"):
            normalize_registration(
                {
                    "email": "ella@example.com",
                    "discoverySource": "x",
                    "consent": True,
                    "company": "spam bot ltd",
                }
            )


if __name__ == "__main__":
    unittest.main()
