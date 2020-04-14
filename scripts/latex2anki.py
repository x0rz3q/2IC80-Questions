from TexSoup import TexSoup
import genanki
import os

LOC = "lectures"

my_model = genanki.Model(
  1607392319,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
])

my_deck = genanki.Deck(2059400110, '2IC80 - Questions')

for tex in os.listdir(LOC):
    if not tex.endswith(".tex"):
        continue

    with open(os.path.join(LOC, tex), 'r') as fp:
        soup = TexSoup(fp.read())

    alls = list(soup.all)

    title = None
    content = ""

    for i in range(1, len(alls)):
        node = alls[i]

        if node.name == 'paragraph':
            if title == None:
                title = node.string
            else:
               note = genanki.Note(model=my_model, fields=[title, content])
               my_deck.add_note(note)
               title = node.string
               content = ""
        elif node.name == 'itemize':
            for item in node.contents:
                item_txt = next(item.contents)
                content += "* {}\n".format(item_txt.strip())
        else:
            if alls[i] is not None:
                content += str(alls[i])

genanki.Package(my_deck).write_to_file('2IC80-Questions.apkg')
