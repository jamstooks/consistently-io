# Todo List

- [ ] travis.yml
- [ ] handle task retry max exceeded! - look into delay compounding
- [ ] 404 + 500 pages
- [ ] reload delayheroku buildpacks:set heroku/python the repo list page if repos are `waiting`
- [ ] snackbar for updates
- [ ] mobile support
- [ ] auto code formatting
- [ ] logging

## Performance

- [ ] Caching
- [ ] Throttling
- [ ] Cache `HasRepoAccess` for a minute or two given the frequency of use
- [ ] `django-pipeline` or `django-compressor` for css

## Down the road...

- [ ] how to handle repo name or ownership changes...
    - there doesn't seem to be a webhook for it, so maybe a scheduled task?
- [ ] eventually offer a "delete history" option
- [ ] off-click listener for menus
- [ ] query analysis and optimizations
- [ ] better icons... number icons can just use a font.
- [ ] GDPR
- [ ] general search + quick search in profile
- [ ] use git secret for webhooks

## Check error conditions
- [ ] integration status in permanant wait


## Next integrations
- [ ] coveralls
- [ ] code climate
- [ ] css validation
- [ ] google page speed insights
