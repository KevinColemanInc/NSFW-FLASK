## NSFW Flask detection

Flask app for detecting NSFW images. Built using the models in [GantMan/nsfw_model](https://github.com/GantMan/nsfw_model) and [bumble-tech/private-detector](https://github.com/bumble-tech/private-detector)

### Requirements
- python 3.8.10

## Quick start

Checkout the [Makefile](./Makefile)

## Slow start

[Deeper dive - NSFW Image detection on Digital Ocean Apps](https://www.kcoleman.me/2022/06/07/nsfw-flask.html)

### prediction v2

```
curl -XPOST 'http://localhost:5000/models/private_detector/predict?url=https://www.kcoleman.me/images/magnify-search.jpg'
{
  "score": 0.006791549269109964,
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

## hosting - Coolify (Docker)

This repository includes a production Dockerfile that Coolify can build directly.
Its runtime-only dependency list keeps the inference image portable across Linux
ARM and x86 hosts; the existing `requirements.txt` remains available for model
training.

1. Create a new **Dockerfile** application in Coolify and point it at this
   repository. Leave the Dockerfile path as `Dockerfile` and set the exposed
   port to `8080`.
2. Configure the health check to use `GET /health`. The first start may take a
   few minutes because the Private Detector model is downloaded before the app
   becomes ready.
3. Use a host with at least 2 GB of RAM. TensorFlow loads the model in every
   Gunicorn worker, so `WEB_CONCURRENCY` defaults to `1`; only raise it when
   additional memory is available.

The downloaded model is cached at `/app/_private_detector_saved_model` inside
the container. To preserve it across deployments, add a Coolify persistent
storage mount at that same path. To use another mount location, set
`PRIVATE_DETECTOR_MODEL_DIR` to its container path. `PORT` is supported when a
different internal port is required.

Build and run it locally:

```bash
docker build -t nsfw-flask .
docker run --rm -p 8080:8080 nsfw-flask
curl http://localhost:8080/health
```

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
