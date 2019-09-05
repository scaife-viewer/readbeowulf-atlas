from graphene import ObjectType, String, relay
from graphene.types import generic
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Fitt, HalfLine, Line, Paragraph, Token, Version


class VersionNode(DjangoObjectType):
    metadata = generic.GenericScalar()

    fitts = DjangoFilterConnectionField(lambda: FittNode)
    paragraphs = DjangoFilterConnectionField(lambda: ParagraphNode)
    lines = DjangoFilterConnectionField(lambda: LineNode)
    halflines = DjangoFilterConnectionField(lambda: HalfLineNode)
    tokens = DjangoFilterConnectionField(lambda: TokenNode)

    class Meta:
        model = Version
        interfaces = (relay.Node,)
        filter_fields = ["name", "urn"]


class FittNode(DjangoObjectType):
    label = generic.GenericScalar()

    paragraphs = DjangoFilterConnectionField(lambda: ParagraphNode)
    lines = DjangoFilterConnectionField(lambda: LineNode)
    halflines = DjangoFilterConnectionField(lambda: HalfLineNode)
    tokens = DjangoFilterConnectionField(lambda: TokenNode)

    class Meta:
        model = Fitt
        interfaces = (relay.Node,)
        filter_fields = ["position", "version__urn"]


class ParagraphNode(DjangoObjectType):
    label = generic.GenericScalar()

    lines = DjangoFilterConnectionField(lambda: LineNode)
    halflines = DjangoFilterConnectionField(lambda: HalfLineNode)
    tokens = DjangoFilterConnectionField(lambda: TokenNode)

    class Meta:
        model = Paragraph
        interfaces = (relay.Node,)
        filter_fields = ["position", "fitt__position", "version__urn"]


class LineNode(DjangoObjectType):
    label = generic.GenericScalar()

    halflines = DjangoFilterConnectionField(lambda: HalfLineNode)
    tokens = DjangoFilterConnectionField(lambda: TokenNode)

    class Meta:
        model = Line
        interfaces = (relay.Node,)
        filter_fields = [
            "position",
            "paragraph__position",
            "fitt__position",
            "version__urn",
        ]


class HalfLineNode(DjangoObjectType):
    label = generic.GenericScalar()

    tokens = DjangoFilterConnectionField(lambda: TokenNode)

    class Meta:
        model = HalfLine
        interfaces = (relay.Node,)
        filter_fields = [
            "position",
            "line__position",
            "paragraph__position",
            "fitt__position",
            "version__urn",
        ]


class TokenNode(DjangoObjectType):
    label = String()

    class Meta:
        model = Token
        interfaces = (relay.Node,)
        filter_fields = [
            "first_in_paragraph",
            "non_verse",
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
            "position",
            "halfline__position",
            "line__position",
            "paragraph__position",
            "fitt__position",
            "version__urn",
        ]


class Query(ObjectType):
    version = relay.Node.Field(VersionNode)
    versions = DjangoFilterConnectionField(VersionNode)

    fitt = relay.Node.Field(FittNode)
    fitts = DjangoFilterConnectionField(FittNode)

    paragraph = relay.Node.Field(ParagraphNode)
    paragraphs = DjangoFilterConnectionField(ParagraphNode)

    line = relay.Node.Field(LineNode)
    lines = DjangoFilterConnectionField(LineNode)

    halfline = relay.Node.Field(HalfLineNode)
    halflines = DjangoFilterConnectionField(HalfLineNode)

    token = relay.Node.Field(TokenNode)
    tokens = DjangoFilterConnectionField(TokenNode)
