# Website

> The following commands assume that you're in /path/to/new_uni directory

## Setup

* Install requirements

    ```
    $ pip3 install -r requirements.txt
    ```

* Migrate database

    ```
    $ python3 manage.py migrate
    ```

* Create super user

    ```
    $ python3 manage.py createsuperuser
    ```

* Update site

    1. Visit `http://your-domain-name/admin`
    2. **Change** (rather than **Add**) `example.com` to your domain name, e.g., `localhost` or `uni.com`

## Usage

* Run Server

    > Make sure that `/etc/nginx/sites-enabled/default` has removed on server, if not:
    > ```
    > $ sudo rm /etc/nginx/sites-enabled/default
    > ```

    * Local for Development

        ```
        $ python3 manage.py runserver
        ```

    * Server for Development

        ```
        $ python3 manage.py collectstatic -c
        ```

    * Server for Production

        ```
        $ python3 manage.py collectstatic -c
        ```
