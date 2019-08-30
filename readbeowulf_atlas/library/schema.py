from graphene import ObjectType, relay
from graphene.types import generic
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Version


class VersionNode(DjangoObjectType):
    metadata = generic.GenericScalar()

    class Meta:
        model = Version
        interfaces = (relay.Node,)
        filter_fields = ["name", "urn"]


class Query(ObjectType):
    version = relay.Node.Field(VersionNode)
    versions = DjangoFilterConnectionField(VersionNode)
