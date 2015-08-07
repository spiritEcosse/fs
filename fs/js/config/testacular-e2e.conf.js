basePath = '../../../';

files = [
  ANGULAR_SCENARIO,
  ANGULAR_SCENARIO_ADAPTER,
  'materials/src/test/e2e/*.coffee'
];

autoWatch = true;

browsers = ['Chrome', 'Firefox'];

singleRun = false;

proxies = {
  '/': 'http://localhost:8000/'
};

junitReporter = {
  outputFile: 'test_out/e2e.xml',
  suite: 'e2e'
};
