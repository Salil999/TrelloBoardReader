import requests
from datetime import datetime


class List:

    def __init__(self, list_id=None, name=None):
        self._id = list_id
        self._name = name
        self._cards = []

    def _add_card(self, card):
        self._cards.append(card)

    def get_name(self):
        return self._name

    def get_cards(self):
        return self._cards

    def __str__(self):
        return self._name

    def __repr__(self):
        return '<ListID {}>'.format(self._id)


class Card:

    def __init__(self, card_id=None, timestamp=None, board_id=None, list_id=None, name=None, url=None):
        self._card_id = card_id
        self._timestamp = timestamp
        self._board_id = board_id
        self._list_id = list_id
        self._name = name
        self._url = url

    def get_card_id(self):
        return self._card_id

    def get_timestamp(self):
        return self._timestamp

    def get_board_id(self):
        return self._board_id

    def get_list_id(self):
        return self._list_id

    def get_text(self):
        return self._name

    def get_url(self):
        return self._url

    def __str__(self):
        return self._name

    def __repr__(self):
        return '<CardID {}>'.format(self._card_id)


class TrelloBoardReader:

    def __init__(self, url):
        # Some really bad URL checking
        if(not url or not isinstance(url, str) or 'trello' not in url):
            raise Exception('Please input in a valid Trello board URL.')
        request = requests.get(url + '.json')

        # Make sure data is actually received
        if(request.status_code != requests.codes.ok):
            raise Exception('Request unsuccessful.')

        self._raw_data = request.json()
        self._organize_data(self._raw_data)

    def _organize_data(self, data):
        if(data['closed']):
            raise Exception('This board seems to be archived.')

        # Board information
        self._board_name = data['name']
        self._board_url = data['url']
        self._board_id = data['id']

        # Method to process lists and THEN cards (must be in this order)
        self._handle_lists(data['lists'])
        self._handle_cards(data['cards'])

    def _handle_lists(self, lists):
        self._lists = set()
        self._list_ids = dict()

        for item in lists:
            if(item['closed']):
                continue

            list_obj = List(list_id=item['id'], name=item['name'])
            self._lists.add(list_obj)
            self._list_ids[item['id']] = list_obj

    def _handle_cards(self, cards):
        for item in cards:
            if(item['closed']):
                continue

            ts = self._format_time(item['dateLastActivity'])
            card_obj = Card(card_id=item['id'],
                            timestamp=ts,
                            board_id=item['idBoard'],
                            list_id=item['idList'],
                            name=item['name'],
                            url=item['url'])
            self._list_ids[item['idList']]._add_card(card_obj)

    def _format_time(self, timestamp):
        return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

    def get_board_name(self):
        return self._board_name

    def get_board_url(self):
        return self._board_url

    def get_board_id(self):
        return self._board_id

    def get_lists(self):
        return list(self._lists)

    def get_list_from_id(self, list_id):
        if(not list_id or list_id not in self._lists):
            raise Exception('Parameter list_id is invalid')
        return self._list_ids[list_id]
