# Download and extract all DBpedia files
mkdir DBpedia_files && cd DBpedia_files
bash download.sh && extract.sh && cd ..

# Download and unzip Apache Jena. It can be used to query/parse the RDF files and save the parse results  
wget https://archive.apache.org/dist/jena/binaries/apache-jena-4.8.0.tar.gz
tar -xzf apache-jena-4.8.0.tar.gz && rm apache-jena-4.8.0.tar.gz

# Check Jena is available. Parse all DBpedia files and merge into one file
cd apache-jena-4.8.0 && bin/riot --version && \
bin/riot --output=Turtle $(find ../DBpedia_files -maxdepth 1 -name '*.ttl') > ../DBpedia_files/dbpedia-2015-10.ttl