
#!/usr/bin/env bash

eb create percolatio-django-core -d --cname "percolatio" --database --database.engine "postgres" --database.size 10 --elb-type application
