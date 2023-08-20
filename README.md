# DBpedia processing tools

This repository contains a set of utility functions to download and process DBpedia dump.

First of all, install the requirements and then run the setup.sh. That will download and extract some of the DBpedia 2015-10 dump files and install Apache Jena to work with RDF data format. Please, ake sure you have enough free space in your computer, since DBpedia dumps files require quite a lot of memory. 

You can always change which specific DBpedia files you want in the download.sh and exract.sh.

After setting up, please also clone the hdt-cpp repo, which we will be using to convert out tutrle format file to hdt format.Mmore info about HDT format at https://www.rdfhdt.org/what-is-hdt/.

```
git clone https://github.com/rdfhdt/hdt-cpp.git

# Go to the hdt-cpp directiry and build a docker image. # Run the container so that it converts combines dbpedia ttl into hdt.
docker build -t hdt .
docker run --rm -v $PWD:/workdir hdt bin/bash -c 'cd workdir && ls && rdf2hdt -f turtle DBpedia_files/dbpedia-2015-10.ttl DBpedia_files/dbpedia-2015-10.hdt'
```

Basically, we are done. There is an example.py script which shows how the processed DBpedia can be used and some utility functions in the KB_utils.

That's all folks! :)
