# Todo List

- [ ] break up react and django repos for testing
- [ ] increase lag on auto-save
- [ ] travis.yml
- [ ] auto code formatting
- [x] analytics
- [x] mobile support
- [x] 404 + 500 pages
- [ ] handle task retry max exceeded! - look into delay compounding
- [ ] reload repo list if repos are `waiting`
- [ ] snackbar for updates
- [ ] logging
- [ ] contributing guide

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
