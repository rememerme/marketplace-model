from models import PhraseCard
from rest_framework import serializers

class PhraseCardSerializer(serializers.ModelSerializer):
    '''
        The PhraseCard serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseCard
        fields = ('phrase_card_id', 'term', 'description', 'order', 'deck')
