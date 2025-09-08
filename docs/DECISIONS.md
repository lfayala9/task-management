# DECISIONS

## (DAY 2)
## Updating this file so late

	ENG: Since the firsts steps as creating the docker compose file and integrating the database were more reading
	the documentation of django and docker and it didn't require any REAL logic decision behind it I did not updated this file until the second day of coding

	ESP: Ya que los primeros pasos fueron crear el docker compose file y integrar de forma basica la db fue mas que todo leer documentación y no requirió ninguna decisión logica real no actualicé este archivo sino hasta la segunda semana de programar

## Not having healthchecks for celery (yet)

	ENG: Being honest because at this stage (second day) I don't really know how celery works really so first I need to fully understeand how it works before having checks that I dont know how they work (also because I didnt find articles or discussions on stackoverflow/reddit that talk about them)

	ESP: Siendo honesto porque en esta etapa de desarrollo no se muy bien aun como funciona celery worker/beat asi que primero necesito entender como funcionan bien esos servicios antes de poner checks que no entiendo como funcionan (tambien porque aun no he encontrado articulos ni discusiones en stackoverflow/reddit que hablen al respecto)

## Advance features (yet to decide)

	ENG: Maybe I'll choose doing the security features because I know how to work with JWT and key management

	ESP: Quizá haga las security features porque ya he trabajado con JWT y key management

## (Day 3)
## Change the views
	
	ENG: It doesn't made any sense what I was doing in the views when calling every single endpoint in a different function instead of doing one layer CRUD and having the templates getting that logic, luckly I watched a youtube video of how to do this efficiently

	ESP: No tenía sentido alguno que estaba llamando cada endpoint en una funcion disnta en vez de tener solo una capa de CRUD que los templates se apoyen en esa logica, menos mal vi un video en youtube de como hacer esto de forma eficiente