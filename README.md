# About
A basic "cloud file storage solution" that uses telegram bots.
  
# Backend

## Env\Config files
For every `.example` file create a corresponding file. `(find . -name "*.example")`

## OAuth
Configure the `DEV_HOST` && `HOST` in the .env file and [google dashboard](https://support.google.com/cloud/answer/6158849?hl=en) accordingly.

## Development
### Without the docker image (make sure the dependencies are available)
 > `optional: poetry config virtualenvs.in-project true`  
 > `poetry install`  
 > `aerich init -t app.db.TORTOISE_ORM`  
 > `aerich init-db`  
 > `uvicorn app:app`

### With docker
> `docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build`  

Backend: http://`${DEV_DOMAIN}`:8080/


## Production

### First install
> `./prod_install.sh`

### Running the dockers
> `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build`  


# Notes
- This is **not** production ready by any standard, this is just a fun idea tested by me :)
- This project is not related in any way to other projects that might have a similar name.