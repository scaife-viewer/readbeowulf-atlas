import abc
import json
import os

from django.conf import settings

from .models import Fitt, HalfLine, Line, Paragraph, Token, Version


LIBRARY_DATA_PATH = os.path.join(settings.PROJECT_ROOT, "data", "library")
LIBRARY_METADATA_PATH = os.path.join(LIBRARY_DATA_PATH, "metadata.json")


class AbstractFactory(abc.ABC):
    idx = 0
    position = 1

    @abc.abstractmethod
    def get(self, **kwargs):
        instance, _ = self.model.objects.get_or_create(
            **{"idx": self.idx, "position": self.position, **kwargs}
        )
        self.idx += 1
        self.position += 1
        return instance


class FittFactory(AbstractFactory):
    model = Fitt

    def get(self, **kwargs):
        return super().get(**kwargs)


class ParagraphFactory(AbstractFactory):
    model = Paragraph

    def get(self, **kwargs):
        return super().get(**kwargs)


class LineFactory(AbstractFactory):
    model = Line

    def get(self, **kwargs):
        return super().get(**kwargs)


class HalfLineFactory(AbstractFactory):
    model = HalfLine

    def get(self, position, **kwargs):
        instance, _ = self.model.objects.get_or_create(
            **{"idx": self.idx, "position": position, **kwargs}
        )
        self.idx += 1
        return instance


def _destructure(token_data):
    fields = (
        "fitt_id",
        "paragraph_id",
        "first_in_paragraph",
        "non_verse",
        "line_id",
        "halfline",
        "position",  # Renamed from token_offset.
        "caesura_boundary",
        "pre_punctuation",
        "text_content",
        "post_punctuation",
        "syntax",
        "parse",
        "lemma",
        "part_of_speech",
        "o",
        "gloss",
        "with_length",
    )
    values = [x if x else None for x in token_data.strip().split("|")]
    token_kwargs = dict(zip(fields, values))

    caesura_boundary = token_kwargs["caesura_boundary"]
    first_in_paragraph = token_kwargs["first_in_paragraph"]
    non_verse = token_kwargs["non_verse"]
    token_kwargs.update(
        {
            "caesura_boundary": True if caesura_boundary == "/" else False,
            "first_in_paragraph": True if first_in_paragraph == "1" else False,
            "non_verse": True if non_verse == "1" else False,
        }
    )

    fitt_ref = token_kwargs.pop("fitt_id")
    paragraph_ref = token_kwargs.pop("paragraph_id")
    line_ref = token_kwargs.pop("line_id")
    halfline_ref = token_kwargs.pop("halfline")

    return fitt_ref, paragraph_ref, line_ref, halfline_ref, token_kwargs


def _prepare_token_obj(
    version_obj, model_lookup, factory_lookup, token_data, token_idx
):
    joins = {"version": version_obj}
    fitt_ref, paragraph_ref, line_ref, halfline_ref, token_kwargs = _destructure(
        token_data
    )

    fitt_obj = model_lookup["fitt"].get(fitt_ref)
    if fitt_obj is None:
        fitt_obj = factory_lookup["fitt"].get(**joins)
        model_lookup["fitt"][fitt_ref] = fitt_obj
    joins.update({"fitt": fitt_obj})

    paragraph_obj = model_lookup["paragraph"].get(paragraph_ref)
    if paragraph_obj is None:
        paragraph_obj = factory_lookup["paragraph"].get(**joins)
        model_lookup["paragraph"][paragraph_ref] = paragraph_obj
    joins.update({"paragraph": paragraph_obj})

    line_obj = model_lookup["line"].get(line_ref)
    if line_obj is None:
        line_obj = factory_lookup["line"].get(**joins)
        model_lookup["line"][line_ref] = line_obj
    joins.update({"line": line_obj})

    key = (line_ref, halfline_ref)
    halfline_obj = model_lookup["halfline"].get(key)
    if halfline_obj is None:
        halfline_obj = factory_lookup["halfline"].get(position=halfline_ref, **joins)
        model_lookup["halfline"][key] = halfline_obj
    joins.update({"halfline": halfline_obj})

    return Token(**{"idx": token_idx, **token_kwargs, **joins})


def _import_version(data):
    version_obj, _ = Version.objects.update_or_create(
        urn=data["urn"],
        defaults=dict(name=data["metadata"]["work_title"], metadata=data["metadata"]),
    )
    full_content_path = os.path.join(LIBRARY_DATA_PATH, data["content_path"])

    factory_lookup = {
        "fitt": FittFactory(),
        "paragraph": ParagraphFactory(),
        "line": LineFactory(),
        "halfline": HalfLineFactory(),
    }
    model_lookup = {"fitt": {}, "paragraph": {}, "line": {}, "halfline": {}}
    tokens_to_create = []

    with open(full_content_path, "r") as f:
        for token_idx, token_data in enumerate(f):
            token_obj = _prepare_token_obj(
                version_obj, model_lookup, factory_lookup, token_data, token_idx
            )
            tokens_to_create.append(token_obj)
    created_count = len(Token.objects.bulk_create(tokens_to_create))
    assert created_count == token_idx + 1


def import_versions(reset=False):
    if reset:
        # Delete all previous Version instances.
        Version.objects.all().delete()

    library_metadata = json.load(open(LIBRARY_METADATA_PATH))
    for version_data in library_metadata["versions"]:
        _import_version(version_data)
