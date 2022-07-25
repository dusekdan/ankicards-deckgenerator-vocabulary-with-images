# AnkiCards Deck Generation

**Goal**: To generate an Anki deck of words + translations provided on the input, enriched by images (enhanced memorization due to linking the word to visual clue).

**How**: List of words and their translations is to be provided on the input, image enrichment will be performed programatically through some web API that provides image for a textual prompt. Sources that use anotated data are prefered over neural net/trained model that generates the image. 

**Output**: Deck foramt that can be imported into Anki desktop app (and then synced to mobile device).

## Anki Format Research

Anki app provides an option to create import files (.txt), in which HTML can be used. <img> with relative path is of interest.

On Windows, Anki stores the resource files in the subdirectory `user/collection.media/` of `%appdata%/anki2`. I need to download and place images into this folder and reference them by their name.

To avoid naming conflicts, pseudorandom string of length 10 will be generated. 

```python
import string
import secrets

def random_string(length=10):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))
```

Anki format for simple "front - back" export file:

```
"item one"  "item two<img src=""imagename.jpg"">"
```

Tab character between items, double-quote `"` envelope to allow for white spaces and HTML tags, escape actual double quotes by doubling the symbol `""`. 

When importing the generated file, allow HTML must be checked. If importing into a new deck rather than to an existing one, check that proper behavior for duplicates is selected (allow duplicates is probably the best setting when you think of "starting new deck that will be the primary one" without actually deleting the old one if something goes wrong).

## Text 2 Image API

API that provides free images without need to mention the author or anything else (distractive for learning): https://www.pexels.com/api/documentation

License: https://www.pexels.com/license/ (All photos and videos on Pexels are free to use., Attribution is not required. Giving credit to the photographer or Pexels is not necessary but always appreciated. You can modify the photos and videos from Pexels. Be creative and edit them as you like.)

### Approach

Use the API search option to find images that correspond to the word being located: 

`https://api.pexels.com/v1/search?query={search_query}&per_page=1&size=small`

And form the response parse out `photos[0].src.tiny` to get a corresponding image.

Documentation shows the API use with API key, but when run from browser, it returns even without API key being provided.

To somewhat adhere to fair use policy (20K requests monthly), account needs to be created and API key provided as a header: `Authorization: API_KEY`

