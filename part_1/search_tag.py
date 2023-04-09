from models import Author, Quote
from mongoengine import connect


connect(host='mongodb+srv://katepomazunova:Dk12345678@cluster0.6ez0nqr.mongodb.net/HW8')

def search_by_name(name):
    autor = Author.objects(fullname__istartswith=name)
    for a in autor:
        quotes = Quote.objects(author=a.id)
        for quote in quotes:
            return quote.quote


def search_by_tag(tag):
    quotes = Quote.objects(tags__istartswith=tag)
    return [quote.quote for quote in quotes]


def search_by_tags(tags):
    quotes = Quote.objects(tags__in=tags)
    return [quote.quote for quote in quotes]


def main():
    while True:

        command = input('Enter "name/tag/tags: text" or "exit":\n >>> ')
        if command.startswith("name:"):
            author_name = command.split(":")[1].strip()
            print(search_by_name(author_name))
        elif command.startswith("tag:"):
            tag = command.split(":")[1].strip()
            print(search_by_tag(tag))
        elif command.startswith("tags:"):
            tags = command.split(":")[1].strip().split(",")
            print(search_by_tags(tags))
        elif command == "exit":
            break
        else:
            print("Invalid command!")


if __name__ == '__main__':
    main()



