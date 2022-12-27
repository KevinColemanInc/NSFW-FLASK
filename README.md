## NSFW Flask detection

Flask app for detecting NSFW images. Built using the models in [GantMan/nsfw_model](https://github.com/GantMan/nsfw_model) and [bumble-tech/private-detector](https://github.com/bumble-tech/private-detector)

### Requirements
- python 3.8.10

## Quick start

Checkout the [Makefile](./Makefile)

## Slow start

[Deeper dive](https://www.kcoleman.me/2021/06/07/nsfw-flask.html)

### prediction

```
curl -XPOST 'https://localhost:5000/predict?url=https://www.kcoleman.me/images/magnify-search.jpg'

{
  "drawings": 0.006791549269109964,
  "hentai": 0.002260813256725669,
  "neutral": 0.9589748978614807,
  "porn": 0.016522442921996117,
  "sexy": 0.015450258739292622
}
```

### prediction v2

```
curl -XPOST 'http://localhost:5000/models/private_detector/predict?url=https://www.kcoleman.me/images/magnify-search.jpg'
{
  "score": 0.006791549269109964,
}
```
or call all models

```
curl -XPOST 'http://localhost:5000/models/all/predict?url=https://www.kcoleman.me/images/magnify-search.jpg' | jq .
{
  "nsfw_model": {
    "drawings": 0.006829037331044674,
    "hentai": 0.0023168271873146296,
    "neutral": 0.958500325679779,
    "porn": 0.017766576260328293,
    "sexy": 0.014587122946977615
  },
  "private_detector": 0.07078268378973007,
  "time": 3.2110581398010254
}
```

### health check
```
curl http://localhost:5000/health

{ "status": "ok }
```
## hosting - FlyIO ~$10/mo

FlyIO is about 50% cheaper than DO for 2GB of RAM, so that is my preference.

```
$ flyctl launch
```

and then

```
$ flyctl deploy
```

You may need to go into the web interface to choose the 2GB RAM offering if the server does not successfully start.

## hosting - Digital Ocean - $20/mo

This works great hosting in "2 GB RAM | 1 vCPU" Digital Ocean box.

sample config:
```yaml
name: nsfw-flask
region: nyc
services:
- environment_slug: python
  github:
    branch: master
    deploy_on_push: true
    repo: KevinColemanInc/NSFW-FLASK
  health_check:
    http_path: /health
  http_port: 8080
  instance_count: 1
  instance_size_slug: basic-s
  name: nsfw-flask
  routes:
  - path: /
  run_command: gunicorn --worker-tmp-dir /dev/shm app:app -t 0
  source_dir: /
```
