
from hypothesis import given
from hypothesis.extra import django

from server.apps.main.models import StarWarsCollection


class StarWarsCollectionPost(django.TestCase):
    """This is a property-based test that ensures model correctness."""

    @given(django.from_model(StarWarsCollection))
    def test_model_properties(self, instance):
        """Tests that instance can be saved and has correct representation."""
        instance.save()

        assert instance.id > 0
        assert len(str(instance)) <= 20
        assert instance.filename == f'{instance.id}.csv'
