'use strict'

### Declare app level module which depends on filters, and services ###

app_name = 'item'
app = angular.module app_name, ["#{app_name}.controllers"]
#["#{app_name}.filters", "#{app_name}.services", "#{app_name}.directives", "#{app_name}.controllers"]

app.config ['$httpProvider', ($httpProvider) ->
  $httpProvider.defaults.xsrfCookieName = 'csrftoken'
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'
]

