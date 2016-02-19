# Installation

## Setup & install

We recommend running the dashboard in a Python [virtual environment](https://virtualenv.readthedocs.org/en/latest/).

Make sure to have [pip](https://pypi.python.org/pypi/pip) installed. Then install virtualenv with:

```
pip install virtualenv
```

After this go to the root dir of this package and create a new virtualenv called 'venv':

```
cd divedashboard-ui
virtualenv venv
```

After the virtualenv has been created, activate it by:

```
. venv/bin/activate
```

Then install the following Python libs with:

```
pip install httplib2
pip install simplejson
pip install flask
pip install rdflib
pip install elasticsearch
```

For the last package it might be necessary to install it manually by downloading the package and running it with:

```
python setup.py install
```

Make sure to remain in the virtualenv when doing this.


## Triple storage & querying

### RDFLib

For querying, Python's RDFLib is used

### ClioPatria

The triplestore used in the CLARIAH project is ClioPatria

## Indexing & search

### ElasticSearch

Currently the indexing is done using [ElasticSearch 2.1.0](https://www.elastic.co/thank-you?url=https://download.elasticsearch.org/elasticsearch/release/org/elasticsearch/distribution/tar/elasticsearch/2.1.0/elasticsearch-2.1.0.tar.gz)

After installation make sure to also install the head plugin for ElasticSearch. This makes it much easier to test your indices

### elasticsearch-pi

To query ElasticSearch from Python [elasticsearch-py](https://elasticsearch-py.readthedocs.org/en/master/) is used.
Install this by downloading the master zip [here](https://github.com/elastic/elasticsearch-py) and then building it using the correct parameters (see their docs).

### Docker

Build docker file:

```
docker build -t dive/dashboard_run . -f Dockerfile
```

Run docker file (mount configuration):

```
docker run --privileged=true -d -p 5504:5504 -v $PWD/your-settings-location/settings.py:/app/settings.py dive/dashboard_run
```
