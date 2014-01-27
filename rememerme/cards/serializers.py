from models import PhraseCard, NominationCard, PhraseDeck, NominationDeck
from rest_framework import serializers

class PhraseCardSerializer(serializers.ModelSerializer):
    '''
        The PhraseCard serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseCard
        fields = ('phrase_card_id', 'term', 'description', 'deck', 'last_modified', 'date_created', 'active')
        
class NominationCardSerializer(serializers.ModelSerializer):
    '''
        The NominationCard serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = NominationCard
        fields = ('nomination_card_id', 'term', 'description', 'deck', 'last_modified', 'date_created', 'active')
        
class PhraseDeckSerializer(serializers.ModelSerializer):
    '''
        The PhraseDeck serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseDeck
        fields = ('deck_id', 'name', 'description', 'last_modified', 'date_created', 'active')

class NominationDeckSerializer(serializers.ModelSerializer):
    '''
        The PhraseDeck serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = NominationDeck
        fields = ('deck_id', 'name', 'description', 'last_modified', 'date_created', 'active')
