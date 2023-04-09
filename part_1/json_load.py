from models import Author, Quote
import json
from mongoengine import connect

connect(host='mongodb+srv://katepomazunova:Dk12345678@cluster0.6ez0nqr.mongodb.net/HW8')

with open('DZ_8/part_1/authors.json', 'r') as jf:
    authors = json.load(jf)

for item in authors:
    author = Author(
        fullname=item.get('fullname'), 
        born_date=item.get('born_date'),
        born_location=item.get('born_location'), 
        description=item.get('description')
        )
    author.save()


with open('DZ_8/part_1/quotes.json', 'r') as jf:
    quotes = json.load(jf)

for item in quotes:
    author = Author.objects(fullname=item.get('author'))
    print(author)
    quote = Quote(
        tags=item.get('tags'), 
        author=author[0].id, 
        quote=item.get('quote')
        )
    quote.save()