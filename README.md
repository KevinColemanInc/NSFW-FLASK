## NSFW Flask detection

Flask app for detecting NSFW images. Built using the models in [GantMan/nsfw_model](https://github.com/GantMan/nsfw_model)

### Requirements
- python 3.8.10

## Quick start
### prediction

```
curl -XPOST 'http://localhost:5000/predict?url=https://www.kcoleman.me/images/magnify-search.jpg'
{
  "drawings": 0.006791549269109964,
  "hentai": 0.002260813256725669,
  "neutral": 0.9589748978614807,
  "porn": 0.016522442921996117,
  "sexy": 0.015450258739292622
}
```
### health check
```
curl http://localhost:5000/health
{ "status": "ok }
```

## hosting - Heroku
It doesn't work b/c the compiled slug size is > 500MB.
## hosting - Digital Ocean

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
  run_command: gunicorn --worker-tmp-dir /dev/shm app:app
  source_dir: /
```