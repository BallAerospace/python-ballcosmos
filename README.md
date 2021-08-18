## Python support for Ball Aerospace COSMOS v4

---

This project allows accessing the COSMOS API from the python programming language.
Additional functionality and support will be added over time.

---

Installation:
```
pip install ballcosmos
```

See the docs and examples for usage

 ## Running the test

```
$ docker-compose -f .\compose.yaml build
$ docker-compose -f .\compose.yaml up -d
Creating network "python-ballcosmos_default" with the default driver
Creating python-ballcosmos_ballcosmos_1 ... done
$ docker exec -it python-ballcosmos_ballcosmos_1 /bin/ash
/app # coverage run -m pytest ./tests/
/app # coverage report
```
