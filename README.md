# Trello Board Reader
Trello Board Reader is a small tool to help you read information from your trello board. The biggest advantage to this tool versus the official API is that you don't need to provide _any_ API keys or any type of authentication. Simple provide the board URL and you should be good to go. __The only limiatation is that the board must be public.__ I'm currently working on a way to make it work for private boards.

## Getting Started
You can install with pip:
- Python: `pip install trello-board-reader`
- Python3: `pip3 install trello-board-reader`

After installing, you can import and use the library. As an example...
```python
from trello_board_reader.reader import TrelloBoardReader

board = TrelloBoardReader('<Enter Trello Board URL here>')
all_lists = board.get_lists()
print(all_lists)

first_list = board.get_list_from_id(all_lists[0])
for card in first_list.get_cards():
    print(card)
```

## Contributing
Throw in a PR and let me know the changes!

## Authors
- [Shashank Saxena](https://shashanksaxena.me)
