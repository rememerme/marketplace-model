'''
    The models and Cassandra serializers for the Game and 
    Requests models to be used in the Game, Requests, Received, and
    Sent APIs. 

    @author: Andy Oberlin, Jake Gregg
'''

from cassa import CassaModel
from django.db import models
import pycassa
from django.conf import settings
import uuid
import random
from rest_framework import serializers

# User model faked to use Cassandra
POOL = pycassa.ConnectionPool('games', server_list=settings.CASSANDRA_NODES)

class PhraseDeck(CassaModel):
    '''
        The Phrase Deck model.
    '''
    
    table = pycassa.ColumnFamily(POOL, 'phrase_deck')
    
    deck_id = models.TextField(primary_key=True)
    description = models.TextField()
    name = models.TextField()
    last_modified = models.DateTimeField()
    date_created = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Game object from a map object with the properties.
        '''
        return PhraseDeck(**mapRep)

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Game object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['deck_id'] = str(cassRep[0])
        
        return PhraseDeck.fromMap(mapRep)
    
    @staticmethod
    def get(deck_id=None):
        '''
            Method for getting a user's Game list from cassandra given the user_id.
        '''
        if deck_id:
            return PhraseDeck.getByID(deck_id)
        
        return None
    
    @staticmethod
    def getByID(deck_id):
        '''
            Gets the user's Game given an ID.
                    
            @param deck_id: The uuid of the deck.
        '''
        if not isinstance(deck_id, uuid.UUID):
            deck_id = uuid.UUID(deck_id)
        return PhraseDeck.fromCassa((str(deck_id), PhraseDeck.table.get(deck_id)))
    
    def save(self):
        '''
            Saves a PhraseDeck given by the cassandra in/output, which is
            a dictionary of values.
        '''
        deck_id = uuid.uuid1() if not self.deck_id else uuid.UUID(self.deck_id)
        PhraseDeck.table.insert(deck_id, CassaPhraseDeckSerializer(self).data)
        self.game_id = str(deck_id)
        
class CassaPhraseDeckSerializer(serializers.ModelSerializer):
    '''
        The PhraseDeck serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseDeck
        fields = ('name', 'description', 'last_modified', 'date_created')


class PhraseCard(CassaModel):
    '''
        The Game model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'phrase_card')
    
    phrase_card_id = models.TextField(primary_key=True)
    description = models.TextField()
    deck = models.TextField()
    term = models.TextField()
    last_modified = models.DateTimeField()
    date_created = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Game object from a map object with the properties.
        '''
        return PhraseCard(**mapRep)

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Game object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['phrase_card_id'] = str(cassRep[0])
        
        return PhraseCard.fromMap(mapRep)
    
    @staticmethod
    def get(card_id=None):
        '''
            Method for getting a user's Game list from cassandra given the user_id.
        '''
        if card_id:
            return PhraseCard.getByID(card_id)
        
        return None
    
    @staticmethod
    def getByID(card_id):
        '''
            Gets the user's Game given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(card_id, uuid.UUID):
            card_id = uuid.UUID(card_id)
        return PhraseCard.fromCassa((str(card_id), PhraseCard.table.get(card_id)))
    
    @staticmethod
    def getRandom(deck_id):
        if not isinstance(deck_id, uuid.UUID):
            deck_id = uuid.UUID(deck_id)
            
        deck_expr = pycassa.create_index_expression('deck', deck_id)
        rand_expr = pycassa.create_index_expression('order', random.randrange(1, 4))
        clause = pycassa.create_index_clause([deck_expr, rand_expr], count=1)
        ans = list(PhraseCard.table.get_indexed_slices(clause))[0]
        return PhraseCard.fromCassa(ans)
    
    def save(self):
        '''
            Saves a PhraseCard given by the cassandra in/output, which is
            a dictionary of values.
        '''
        card_id = uuid.uuid1() if not self.phrase_card_id else uuid.UUID(self.phrase_card_id)
        PhraseCard.table.insert(card_id, CassaPhraseCardSerializer(self).data)
        self.phrase_card_id = str(card_id)

class CassaPhraseCardSerializer(serializers.ModelSerializer):
    '''
        The PhraseCard serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseDeck
        fields = ('deck', 'description', 'term', 'last_modified', 'date_created')


class NominationDeck(CassaModel):
    '''
        The Phrase Deck model.
    '''
    
    table = pycassa.ColumnFamily(POOL, 'nomination_deck')
    
    deck_id = models.TextField(primary_key=True)
    description = models.TextField()
    name = models.TextField()
    last_modified = models.DateTimeField()
    date_created = models.DateTimeField()
    
    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Game object from a map object with the properties.
        '''
        return NominationDeck(**mapRep)

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Game object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['deck_id'] = str(cassRep[0])
        
        return NominationDeck.fromMap(mapRep)
    
    @staticmethod
    def get(deck_id=None):
        '''
            Method for getting a user's Game list from cassandra given the user_id.
        '''
        if deck_id:
            return NominationDeck.getByID(deck_id)
        
        return None
    
    @staticmethod
    def getByID(deck_id):
        '''
            Gets the user's Game given an ID.
                    
            @param deck_id: The uuid of the deck.
        '''
        if not isinstance(deck_id, uuid.UUID):
            deck_id = uuid.UUID(deck_id)
        return NominationDeck.fromCassa((str(deck_id), NominationDeck.table.get(deck_id)))

    def save(self):
        '''
            Saves a PhraseCard given by the cassandra in/output, which is
            a dictionary of values.
        '''
        deck_id = uuid.uuid1() if not self.deck_id else uuid.UUID(self.deck_id)
        NominationDeck.table.insert(deck_id, CassaNominationDeckSerializer(self).data)
        self.deck_id = str(deck_id)
            
class CassaNominationDeckSerializer(serializers.ModelSerializer):
    '''
        The NominationDeck serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseDeck
        fields = ('deck_id', 'name', 'description', 'last_modified', 'date_created')
    
class NominationCard(CassaModel):
    '''
        The Game model to support the API.
    '''
    table = pycassa.ColumnFamily(POOL, 'nomination_card')
    
    nomination_card_id = models.TextField(primary_key=True)
    description = models.TextField()
    deck = models.TextField()
    term = models.TextField()
    last_modified = models.DateTimeField()
    date_created = models.DateTimeField()

    @staticmethod
    def fromMap(mapRep):
        '''
            Creates a Game object from a map object with the properties.
        '''
        return NominationCard(**mapRep)

    @staticmethod
    def fromCassa(cassRep):
        '''
            Creates a Game object from the tuple return from Cassandra.
        '''
        mapRep = {key : val for key, val in cassRep[1].iteritems()}
        mapRep['nomination_card_id'] = str(cassRep[0])
        
        return NominationCard.fromMap(mapRep)
    
    @staticmethod
    def get(card_id=None):
        '''
            Method for getting a user's Game list from cassandra given the user_id.
        '''
        if card_id:
            return NominationCard.getByID(card_id)
        
        return None
    
    @staticmethod
    def getByID(card_id):
        '''
            Gets the user's Game given an ID.
                    
            @param user_id: The uuid of the user.
        '''
        if not isinstance(card_id, uuid.UUID):
            card_id = uuid.UUID(card_id)
        return NominationCard.fromCassa((str(card_id), NominationCard.table.get(card_id)))
    
    def save(self):
        '''
            Saves a NominationCard given by the cassandra in/output, which is
            a dictionary of values.
        '''
        card_id = uuid.uuid1() if not self.nomination_card_id else uuid.UUID(self.nomination_card_id)
        NominationCard.table.insert(card_id, CassaPhraseCardSerializer(self).data)
        self.nomination_card_id = str(card_id)
    
class CassaNominationCardSerializer(serializers.ModelSerializer):
    '''
        The NominationCard serializer used to create a python dictionary for submitting to the
        Cassandra database with the correct options.
    '''
    class Meta:
        model = PhraseDeck
        fields = ('deck', 'description', 'term', 'last_modified', 'date_created')
