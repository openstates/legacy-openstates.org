Issues?
-------

Issues with the opencivicdata.org API should be filed at the [api.opencivicdata.org issue tracker](https://sunlight.atlassian.net/browse/OCD/component/10001)

All Open Civic Data issues can be browsed and filed at [the Open Civic Data JIRA instance](https://sunlight.atlassian.net/browse/OCD/).

What is this?
-------------

This repo is essentially just a Django project for deployment- actual API code is a part of several other projects:

* [boundaries](https://github.com/rhymeswithcycle/represent-boundaries) - backs GIS portion
* [imago](https://github.com/opencivicdata/imago) - people, bills, events, etc.


To get started:

    fab postgres_install
    fab postgres_createdb
    fab ocdapi_download
    fab ocdapi_syncdb
    fab ocdapi_install_app
    fab ocdapi_install_server
