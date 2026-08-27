# workstreams/WF-105/test_boundary_policy.py — Contract coverage for the Non-DNA isolation boundary.
#
# VERSION HISTORY
# v1.0.0 · 2026-08-23 · Initial version: proves public denial, private research access, and visible lineage requirements.

import unittest

from boundary_policy import NON_DNA_DOMAIN, PUBLIC_SURFACES, authorize_domain, validate_research_envelope


class BoundaryPolicyTests(unittest.TestCase):
    def test_every_public_surface_rejects_non_dna(self) -> None:
        for surface in PUBLIC_SURFACES:
            with self.subTest(surface=surface):
                self.assertFalse(authorize_domain(surface, NON_DNA_DOMAIN, role="researcher"))

    def test_private_research_surface_requires_research_role(self) -> None:
        self.assertTrue(authorize_domain("internal_what_if", NON_DNA_DOMAIN, role="researcher"))
        self.assertFalse(authorize_domain("internal_what_if", NON_DNA_DOMAIN, role="public"))

    def test_valid_research_envelope_is_accepted(self) -> None:
        validate_research_envelope({"data_domain": NON_DNA_DOMAIN, "research_only": True, "warning": "Not DNA strategy performance.", "source_window": "2026-01-01/2026-06-30", "methodology_version": "1.0.0", "generated_at": "2026-08-23T19:48:00+01:00"})

    def test_missing_warning_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            validate_research_envelope({"data_domain": NON_DNA_DOMAIN, "research_only": True, "source_window": "x", "methodology_version": "1", "generated_at": "now"})

    def test_dna_domain_remains_available_to_public_surface(self) -> None:
        self.assertTrue(authorize_domain("strategy_directory", "DNA_DIRECTORY", role="public"))


if __name__ == "__main__":
    unittest.main()

