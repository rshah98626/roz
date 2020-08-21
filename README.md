# Roz
The secretary, and hopefully the monolith, of all applications.

### Setting up the Virtual Environment
1. First make sure pyenv and pyenv-virtualenv are installed (add links)
2. Then run `pyenv virtualenv 3.7.7 myvenv` to add the correct python version.
3. Next, run `pyenv local 3.6.8` in the root of the repository.
4. To setup your virtualenv, run
```
$ pip install virtualenv
$ virtualenv .venv
$ pip install -r requirements.txt
```

Make sure to enter the virtualenv by running `source ./.venv/bin/activate`

### Running the App
First, make sure to check out the Chatty README to setup the necessary containers.
Then start the server by running `python manage.py runserver`.

### Testing
Run the entire test suite with `python manage.py test`.
Here are a couple other handy testing commands:
```
# Test the coverage of the tests
$ coverage run --source='.' manage.py test

# Show the coverage report
$ coverage report

# Run a certain test module (in this case the profile route test)
$ python manage.py test users.tests.routes.test_profile_route
```

### Next Steps
Be sure to checkout the app-specific README for what other steps need to be taken to get ready to code!
