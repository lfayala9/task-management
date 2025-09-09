# DECISIONS

## FEATURES MADE

## JWT

	ENG: Decided to implement the extra feature of JWT authentication with refresh tokens because I already know a thing or two of JWT and theres a lot of documentation. JWT in that sense is really practical and scalable, thus separing the different contexts as web users with cookies and CSRF and API users with bearable tokens is a mixed integration that works really well in this context


## FEATURES SKIPPED

	ENG: I skipped every extra feature besides the JWT one because I was running out of time and I spend a lot of time doing the mandatory part. Poor time administration I guess


## Time allocation breakdown

	ENG:
	First day: Learning about dockerfiles and compose and assembling the docker-compose file with everything we needed, also, despite knowing a thing or two about django I used a lot of time reading the docs, watching tutorials and researching about it.

	Second day: I kinda started building the house by the roof and first I did the views and used the django templates to generate a html, also created a basic task model to ensure that the html could render every request I needed

	Third day: I built almos all models and tested them with creating the task and assign it to a ceratin user also, since I started from the finishing point, that night I started to create the REST architecture and testing some API REST endpoints

	Fourth Day: Pure REST tests with all endpoints and researching reading and doing my best with Celery

## Styles

	ENG: I have every single html with a style tag, despite it being ugly I leave it that way beacuse its specified that the frontend part its not that relevant, and django dropped a MIME Type error that I couldnt know how to fix


