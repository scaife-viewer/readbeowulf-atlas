import json
import os

from django.conf import settings

from .models import Version


LIBRARY_DATA_PATH = os.path.join(settings.PROJECT_ROOT, "data", "library")
LIBRARY_METADATA_PATH = os.path.join(LIBRARY_DATA_PATH, "metadata.json")


def _import_version(data):
    version_obj, _ = Version.objects.update_or_create(
        urn=data["urn"],
        defaults=dict(name=data["metadata"]["work_title"], metadata=data["metadata"]),
    )
    full_content_path = os.path.join(LIBRARY_DATA_PATH, data["content_path"])

    with open(full_content_path, "r") as f:
        for line_idx, line in enumerate(f):
            raise NotImplementedError()


def import_versions(reset=False):
    if reset:
        # Delete all previous Version instances.
        Version.objects.all().delete()

    library_metadata = json.load(open(LIBRARY_METADATA_PATH))
    for version_data in library_metadata["versions"]:
        _import_version(version_data)
