module.exports = function(config){
    config.set({
        preprocessors: {
            'materials/src/coffee/*.coffee': ['coffee'],
            'materials/src/test/**/controllersSpec.coffee': ['coffee']
        },

        basePath : '../../../',

        files : [
            'static/assets/bower_components/angular/angular.js',
            'static/assets/bower_components/angular-route/angular-route.js',
            'static/assets/bower_components/angular-resource/angular-resource.js',
            'static/assets/bower_components/angular-animate/angular-animate.js',
            'static/assets/bower_components/angular-mocks/angular-mocks.js',
            'materials/src/coffee/*.coffee',
            'materials/src/test/**/controllersSpec.coffee'
        ],

        coffeePreprocessor: {
            // options passed to the coffee compiler
            options: {
                bare: true,
                sourceMap: false
            },
            // transforming the filenames
            transformPath: function(path) {
                return path.replace(/\.coffee$/, '.js')
            }
        },

        autoWatch : true,

        frameworks: ['jasmine'],

        browsers : ['Chrome', 'Firefox'],

        plugins : [
            'karma-coffee-preprocessor',

            'karma-chrome-launcher',
            'karma-firefox-launcher',
            'karma-jasmine'
        ],

        junitReporter : {
            outputFile: 'test_out/unit.xml',
            suite: 'unit'
        }

    });
};