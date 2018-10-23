# Todo List

- [ ] store travis build data for quick linking
- [ ] handle task retry max exceeded! - look into delay compounding
- [x] is HTML Validation delay working?
- [ ] reload repo list page if repos are `waiting`
- [ ] snackbar for updates
- [ ] logging
- [ ] contributing guide
- [x] Repo BADGES!! https://github.com/google/pybadges
 - [ ] confirm caching https://github.com/github/markup/issues/224
- [ ] add license
- [ ] should users be able to set numeric goals, like coverage percentage?

## Performance

- [ ] Caching
- [ ] Throttling
- [ ] Cache `HasRepoAccess` for a minute or two given the frequency of use
- [ ] `django-pipeline` or `django-compressor` for css
- [ ] query optimizations

## Down the road...

- [ ] GDPR
 - [ ] offer a "delete history" option
- [ ] how to handle repo name or ownership changes...
    - there doesn't seem to be a webhook for it, so maybe a scheduled task?
- [ ] off-click listener for menus
- [ ] query analysis and optimizations
- [ ] better icons... number icons can just use a font.
- [ ] general search + quick search in profile
- [ ] use git secret for webhooks
- [ ] auto code formatting w/ prettier
- [ ] store and display the commit message

## Check error conditions
- [ ] integration status in permanant wait

## Next integrations
- [x] [coveralls](https://docs.coveralls.io/api-introduction)
- [ ] [codecov](https://docs.codecov.io/reference#section-get-a-single-commit)
- [ ] [google page speed insights](https://developers.google.com/speed/docs/insights/v4/getting-started)
- [ ] [code climate](https://developer.codeclimate.com/#repositories)
- [ ] css validation
- [ ] issue tracking?
- [ ] code velocity?
