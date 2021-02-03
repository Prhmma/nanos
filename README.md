# Nanos

There are methods to calculate word similarity, and most of them are dictionary-based. Besides, similarity metrics must be considered. I used the `WUP` similarity score. more information about similarity metrics are available here (https://www.nltk.org/howto/wordnet.html)

There are 2 interfaces to use, a CLI version, and a web app for more interactive use.
# Installation
First, install the requirements:
## Python 3.x

    https://docs.python-guide.org/starting/install3/linux/
## Libraries
```sh
pip install bs4
pip install nltk
pip install flask
pip install WordCloud
pip install matplotlib
pip install validator_collection
```
### notice:
Make sure to have required NLTK data. Downloading process embeded in the code, but in some OS distribution, need to download manualy.
```py
import nltk
nltk.download("wordnet")
nltk.download("words")
```
# Running
## cli
```sh
cd nanos
sudo python3 cli.py
```
## web app
```sh
cd nanos
sudo python3 app.py
```
then a web browser should open manualy, and visit this link (127.0.0.1:5000)

# How it works
## Web app
<b> URL: </b> Must be a valid URL starts with `http: //` or `https: //`

<b> Products / Services: </b> String contains one or more words, sperated by `space` or`, `. cannot left empty.

<b> Similarity Percentage: </b> This slider determines how much similarity is desired. After fetching data from the URL, moving this slider will help see results with more / less similarity score.

<b> Fetch: </b> After completing the required fields, this button needs to be pressed. There is no loading available, so the user must make sure the URL is fetched completely with the browser loading system.

<b> Refresh: </b> If `fetch` return no results, the user must use this button to refresh the HTML elements and see the results. this is needed because I am an HTML noob and did not figure out how to use `AJAX` and dynamic load.

![alt text](img\Capture.JPG)

# Bonus
There is a concept called `Word Cloud`. This diagram design to show words based on their frequency. I used it to show similarity instead of frequency. The bigger the word, The greater its similarity to the given `Products/Services`


# Project Structure
this project made of 3 main python files, an HTML index file in `templates` and this README file.
Proper documentation tried to be provided in the code.

-   similarity.py: Main class with required methods.

-   app.py: Flask web app interface

-   cli.py: command based interface

Implemented as partial fulfillment of Nanos hiring process requirements.
prhmma@gmail.com