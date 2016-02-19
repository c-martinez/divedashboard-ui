# DIVE Dashboard Front-end

The DIVE Dashboard front-end code is separate from the back-end code, which is located [here](https://github.com/cwmeijer/divedashboard). Currently this codebase includes a custom back-end for testing purposes. Over time however, the idea is to only use the indicated back-end.

## Prerequisites:


### Bower


Bower is a package manager for the web.

Download it [here](http://bower.io/)

You might need to install [npm](https://www.npmjs.com/) in order to get Bower installed.

Then make sure to run the following commands project's root directory (`.bowerrc` ensures that files are stored in the correct location under `/src/static` directory).

```
bower install
```


### Compass

Compass is a CSS authoring framework.

Download it [here](http://compass-style.org/)

Follow the install instructions [here](http://compass-style.org/install/)

After installation it is possible to run the following command in **/src/static**:

```
compass watch
```

Whenever you make changes to the SASS files (in **/src/static/sass**), the file main.css is automatically updated.


### Python (libraries)

The back-end (webserver) code is written using Python 2.7.

In order to run the [Flask](http://flask.pocoo.org/) server, check out the docs/INSTALL.md


## Configuring the server

If all required packages have been installed. Go to the **/src** directory and make sure to copy the **settings-example.py** file into a new file called **settings.py**.

Make sure that the variables entered in the example would be suitable for your local environment. If so, it should be possible to start the server.

Note: For the moment, please obtain the API information from the DIVE+ consortium

## Running the server

Go to **/src** and start the server by running:

```
python server.py
```
