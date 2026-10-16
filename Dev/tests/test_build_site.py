import json
import re
import tempfile
import unittest
from pathlib import Path

from Dev.scripts.build_site import build_site


class BuildSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        (self.repo / "Dev" / "site").mkdir(parents=True)
        (self.repo / "Dev" / "site" / "index.html").write_text("master", encoding="utf-8")
        (self.repo / "Dev" / "site" / "styles.css").write_text("styles", encoding="utf-8")
        (self.repo / "Dev" / "site" / "app.js").write_text("app", encoding="utf-8")
        self.collection = self.repo / "All Files" / "Finance"
        self.collection.mkdir(parents=True)
        (self.repo / "Dev" / "sources.json").write_text(
            json.dumps(
                {
                    "schemaVersion": 1,
                    "collections": [
                        {
                            "sourceRepository": "Finance-Source",
                            "sourceUrl": "https://example.test/Finance-Source",
                            "sourceCommit": "abc123",
                            "path": "All Files/Finance",
                            "category": "portals",
                            "title": "Finance Manager",
                            "description": "Finance designs",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        self.output = self.repo / "_site"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_unicode_and_spaces_are_percent_encoded_in_artifact_url(self):
        (self.collection / "ILMA – Student Fees.html").write_text(
            "<title>Student Fees</title>", encoding="utf-8"
        )

        catalog = build_site(self.repo, self.output)

        self.assertEqual(
            catalog["items"][0]["url"],
            "All%20Files/Finance/ILMA%20%E2%80%93%20Student%20Fees.html",
        )

    def test_missing_html_title_falls_back_to_readable_filename(self):
        (self.collection / "ILMA_CMS_Approval_Requests_mockup.html").write_text(
            "<main>No title element</main>", encoding="utf-8"
        )

        catalog = build_site(self.repo, self.output)

        self.assertEqual(catalog["items"][0]["title"], "ILMA CMS Approval Requests")

    def test_same_filename_in_different_folders_has_unique_artifact_id(self):
        (self.collection / "first").mkdir()
        (self.collection / "second").mkdir()
        (self.collection / "first" / "Dashboard.html").write_text(
            "<title>Dashboard</title>", encoding="utf-8"
        )
        (self.collection / "second" / "Dashboard.html").write_text(
            "<title>Dashboard</title>", encoding="utf-8"
        )

        catalog = build_site(self.repo, self.output)

        ids = [item["id"] for item in catalog["items"]]
        self.assertEqual(len(ids), 2)
        self.assertEqual(len(set(ids)), 2)

    def test_supported_file_added_to_collection_is_discovered_automatically(self):
        (self.collection / "New Prototype.html").write_text(
            "<title>New Prototype</title>", encoding="utf-8"
        )
        (self.collection / "Guide.docx").write_bytes(b"document")

        catalog = build_site(self.repo, self.output)

        self.assertCountEqual(
            [(item["title"], item["kind"]) for item in catalog["items"]],
            [("Guide", "document"), ("New Prototype", "prototype")],
        )

    def test_unknown_placeholders_are_copied_but_not_cataloged(self):
        (self.collection / "tmp").write_text("x", encoding="utf-8")
        (self.collection / "Prototype.html").write_text(
            "<title>Prototype</title>", encoding="utf-8"
        )

        catalog = build_site(self.repo, self.output)

        self.assertEqual(len(catalog["items"]), 1)
        self.assertTrue(
            (self.output / "All Files" / "Finance" / "tmp").exists()
        )

    def test_site_shell_and_catalog_are_written_to_output(self):
        (self.collection / "Prototype.html").write_text(
            "<title>Prototype</title>", encoding="utf-8"
        )

        build_site(self.repo, self.output)

        self.assertEqual((self.output / "index.html").read_text(), "master")
        written_catalog = json.loads(
            (self.output / "catalog.json").read_text(encoding="utf-8")
        )
        self.assertEqual(written_catalog["stats"]["prototypes"], 1)

    def test_prototype_has_stable_path_based_preview_filename(self):
        (self.collection / "Prototype.html").write_text(
            "<title>Prototype</title>", encoding="utf-8"
        )

        catalog = build_site(self.repo, self.output)

        self.assertEqual(
            catalog["items"][0]["preview"],
            "previews/eb700f82a96f2c9f.webp",
        )

    def test_prototypes_appear_before_documents_in_visual_library(self):
        (self.collection / "A Guide.docx").write_bytes(b"document")
        (self.collection / "Z Prototype.html").write_text(
            "<title>Z Prototype</title>", encoding="utf-8"
        )

        catalog = build_site(self.repo, self.output)

        self.assertEqual(
            [item["kind"] for item in catalog["items"]],
            ["prototype", "document"],
        )

    def test_live_filter_buttons_match_configured_categories(self):
        repo_root = Path(__file__).resolve().parents[2]
        sources = json.loads((repo_root / "Dev" / "sources.json").read_text())
        categories = {item["category"] for item in sources["collections"]}
        shell = (repo_root / "Dev" / "site" / "index.html").read_text()
        filters = set(re.findall(r'data-filter="([^"]+)"', shell))

        self.assertEqual(filters, {"all", *categories})


if __name__ == "__main__":
    unittest.main()
