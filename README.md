
# Purpose of the project

University project.
This django project is a small e-commerce about manga and anime (I called it MangaStore).
I tried to make it like a real store website but it doesn't have some 'real' features:

- Payment system is a fake one, for example it doesn't check the card number.
- Not-in-stock products doesn't exist for simplicity reasons.


# Dependencies

I used poetry virtual environment 1.1.14 version; It is not mandatory to use this venv.
If you check in the pyproject.toml file You will see all the dependencies I used.
If You don't know how to use or download poetry please follow the instructions in [Poetry guide](https://python-poetry.org/docs/).
After installing poetry you simply have to run this commands:
`py -m poetry init`, this is to init the project in poetry environment
`py -m poetry install`, this is to install all the dependencies and to create the environment

If something goes wrong please check the Poetry documentation or other sites that can help You.



# Running the project

After installing all the dependencies You can finally try to run the project.
I do that by doing:
`cd core`, this is to be sure I am in the right directory where I put *manage.py*
`py -m poetry run py -m manage runserver`, this is to run the server

I must use *py -m* before poetry because my OS doesn't recognize the command *poetry*, if You don't seem
to have this problem You can simply use poetry at the begginning of the command.
Notice that if You are in the poetry shell, the project won't be able to run.
Notice that py -m manage is used instead of py manage.py, to see the differences go to the [python documentation](https://docs.python.org/3/using/cmdline.html).

After this point You should be able to see the website in the following internet [page](http://127.0.0.1:8000/).
If You want to use one of the already-made-user You can find the accounts (with passwords ad fake email) in the account.txt file.



# Directory and Files

Inside the /core directory You can find all the project's files and directories I used (You never said).

### Directory

- **/account**, represents the accounts
    + **/migrations**, contains the database migrations of the accounts
    + **admin.py**, register UserBase for the admin user
    + **forms.py**, forms for registration, login and to edit the user's profile
    + **models.py**, creates new user and models UserBase
    + **urls.py**, url for the app *account* that begins with *account/*
    + **views.py**, renders the dashboard functionality (ex. edit profile), registration and login

- **/cart**, represents the cart of user session
    + **/migrations**, contains the database migrations of the cart
    + **cart.py**, represents the class of the cart and has the methods to change the content
    + **urls.py**, url for the app *cart* that begins with *cart/*
    + **views.py**, renders the cart summary

- **/core**, the core of the project 
    + **settings.py**, the settings of the project
    + **tests.py**, tests some features of the project like the view of the cart
    + **urls.py**, where the application starts to search a url

- **/htmlcov**, used to study the coverage of tests in the project
    for more information open the index.html file
    If You want to use the coverage command You can see the [documentation](https://coverage.readthedocs.io/en/6.4.2/).

- **/media/images**, where the image of the products are saved

- **/orders**, represents the orders done by the users 
    + **/migrations**, contains the database migrations of the cart
    + **admin.py**, register the Order and OrderItem objects
    + **models.py**, models the orders' objects
    + **urls.py**, url for the app *orders* that begins with *orders/*
    + **views.py**,  redners the orders story of a user

- **/payment**, represents the payment method
    + **urls.py**, url for the app *payment* that begins with *payment/*
    + **views.py**, renders if the order is already been payed or not

- **/static**, static file to render html

- **/store**,
    + **/migrations**, contains the database migrations of the store
    + **admin.py**, register the Product, Category and Review objects
    + **forms.py**, forms how to add a new object in the seller/admin views
    + **models.py**, models the product, category and review objects
    + **testModels.py**, tests the models in the models.py file
    + **testViews.py**, tests some of the view in the views.py file
    + **urls.py**, url for the app *store* that begins with *store/*
    + **views.py**, renders how should be seen and how to creates all the models in models.py file

- **/templates**, for every application there is a directory with the templates used in the project.
    In the /templates/store there is the base.html that is inherited from all the others templates. 

### Files

- **manage.py**, file used to start the project, the server and the applications.
    If You don't know how to use this just type `py -m poetry run py -m manage` or `poetry run py -m manage`.


# Other 
If You have truble with my project You can text me in the issue part of Github.
If You have problems with a dependencies in my project I, again, reccommend You to see StackOverflow or the documentation of the dependency.


**I am sorry for my english, but I hope this readme will help You.**
**Thanks a lot if You clone or find bugs or use this project ^-^**

