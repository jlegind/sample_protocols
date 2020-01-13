# sample_protocols
analysis of dataset metadata in order to indentify and machine tag these accordingly


The GBIF API can return free text like fuzzy searches like:
http://api.gbif.org/v1/dataset/search?q=lter 

Here the search term is lter (Long Term Ecological Monitoring) which shows up quite a lot as a label for Sample Event datasets.
We need to look through the dataset metadata to explore whether the term shows up. THen we can create a list or csv file of _candidate_ datasets for machine taggging.

