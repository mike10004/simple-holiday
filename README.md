Simple Holiday Giving Assignment Generator
==========================================

This is a program that generates assignments of gifts for a group of people 
where the total number of gifts given/received by any person is bounded below
the total number of people in the group.

The idea is to reduce burden and inefficiency of holiday gift giving by 
simplifying and randomizing the giving. 

Say you have 5 people, you might decide that each person will give and receive 
2 gifts, and the assignment generator will generate random assignments of 
giver to recipient. The generator tries to avoid situations like one person 
being assigned multiple gifts to one other person, or having people exchange 
gifts (A->B and B->A), where possible.

To generate your own, fork this repo and execute

    $ python3 -m roundrobin.assignment \
        --format tsv_slots \
        --slots GivesTo1 GivesTo2 \
        -- Happy Grumpy Sleepy Sneezy Doc

The output might be like this:

            GivesTo1  GivesTo2
    Happy   Grumpy    Doc
    Grumpy  Doc       Sleepy
    Sleepy  Sneezy    Happy
    Sneezy  Happy     Grumpy
    Doc     Sleep     Sneezy

Other formats are possible with the `--format` option. Execute `--help` for details.

Markdown-format tables can be rendered here: https://www.tablesgenerator.com/markdown_tables
