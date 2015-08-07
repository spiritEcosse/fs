basePath = '../../../';

files = [
  JASMINE,
  JASMINE_ADAPTER,
  'static/assets/bower_components/angular/angular.js',
  'static/assets/bower_components/angular/angular-*.js',
  //'materials/src/test/lib/angular/angular-mocks.js',
  'materials/src/test/**/*Spec.coffee',
  'materials/src/coffee/*.coffee'
  //'materials/src/coffee/services.coffee',
  //'materials/src/coffee/controllers.coffee',
  //'materials/src/coffee/filters.coffee',
  //'materials/src/coffee/directives.coffee',
  //'materials/src/coffee/app.coffee',
];

autoWatch = true;

browsers = ['Chrome', 'Firefox'];

junitReporter = {
  outputFile: 'test_out/unit.xml',
  suite: 'unit'
};
