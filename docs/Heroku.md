# Heroku Config

We need three buildpacks:

    heroku buildpacks:set heroku/python
    heroku buildpacks:add --index 1 heroku/nodejs
    heroku buildpacks:add --index 1 https://github.com/dmathieu/heroku-buildpack-submodules

We're using `heroku-buildpack-submodules` to ensure that the
git submodules get pulled during github sync.
