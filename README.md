# The Civil War in Syria

[Research Proposal based on this data](https://docs.google.com/document/d/1JcYInMT4fDYMPdmvJYAiZjEA5KkklTwUUmUY-SbB2MU/edit?usp=sharing)


Here's a link to a [visualization of refugee flow](https://www.lucify.com/the-flow-towards-europe/  )

And here's the [GitHub page for that project](https://github.com/lucified/lucify-refugees  ).


The VDC dataset has already been scraped, and that's the dataframe that's being used right now. Here's the link to that site:

http://vdc-sy.net/en/


HRDAG
An organization that posted their methodology for removing duplicates, among oter stuff. Ther page about SYria is linked to here:

https://hrdag.org/syria/

And their actual technical memo is here:

https://hrdag.org/wp-content/uploads/2016/07/HRDAG-AI-memo.pdf



Things to do:

A number of dataframes failed to combine due to duplicate columns that are not beiong renamed with the rename_dup_cols() function for some reason. These dataframes can be loaded with  load('failed_df'). Once columns are renamed such that there are no duplicate names, they can be combined with combine_dataframes.

The all_df needs a lot of wrangling work. The are multiple duplicate columns that should be combined together. There are also some entries that have some kind of text encoding/decoding errors. Some functions should be made to view all this information quickly and easily.

all_df contains a lot of information in the notes section, as well as more acute location data.

Our current dataframe only goes to August 2018, which means I missed out some data while scraping. I believe I have a fix for this already, but I need to check data scraped on a different computer.

We will probably need to use geopandas to display provincial data for Syria. I found some shape files here: 

https://data.humdata.org/dataset/syrian-arab-republic-administrative-boundaries-populated-places

They can also be found in the repo here. We will be using the adm1 map, since that is the shape file for provinces.

We will also eventually want to scrape this site: 

https://csr-sy.org/?id=182&sons=redirect&l=1&

So that can be looked into now as well.

My line of progress looks like this:

Explore dataset (really just reading a bunch of entries)
Start cleaning VDC dataset
Get maps working with geopandas
Visualize data over map
Create animation over time

Scrape second datset and repeat the process above.

This project can be seen as either a web scraping, data wrangling, or data visualization project depending on what you want focus on.

There are a lot of different ways we can go about this project, so please let me know of any ideas that you have while working with/thinking about this data.

Let me know if you have any questions by emailing me at rsul@ucsc.edu or by responding in the canvas discussion page. 

There is a lot of work that can be done for this project, so if people are motivated to join this group there is plenty of work to go around.
