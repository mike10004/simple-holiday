Simple Holiday Giving Assignment Generator
==========================================

To generate your own, fork this repo and configure your Travis build 
environment with the following variables:

* `HOLIDAY_GIVERS` - `"Larry Moe Curly"` is 3 people
* `HOLIDAY_SLOTS` - `"borrowed blue"` is 2 gift types
* `HOLIDAY_SEED` - an integer that seeds the randomizer

Markdown-format tables can be rendered at 
https://www.tablesgenerator.com/markdown_tables

When executing from the command line, you may have to do

    $ export PYTHONPATH=$(pwd)

first.