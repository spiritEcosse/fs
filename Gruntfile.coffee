module.exports = (grunt) ->
    grunt.initConfig(
        pkg: grunt.file.readJSON('package.json')
        coffee:
            files:
                src: ['materials/src/coffee/**/*.coffee']
                dest: 'static/assets/materials/js/script.js'
        less:
            production:
                options:
                    paths: ["assets/css"],
                    sourceMap: true
                files:
                    "static/src/css/main.css": "static/src/less/main.less",
                    "static/oscar/css/styles.css": "static/oscar/less/styles.less",
        cssmin:
            dist:
                files:
                    'static/build/css/style.min.css': ['static/bower_components/lightslider/dist/css/lightslider.css',
                        'static/bower_components/yamm/assets/css/yamm.css',
                        "static/djangular/css/bootstrap3.css",
                        "static/djangular/css/styles.css",
                        "static/bower_components/bootstrap-select/dist/css/bootstrap-select.min.css",
                        'static/oscar/css/styles.css',
                        'static/src/css/**/*.css',
                    ],

    )

    grunt.loadNpmTasks('grunt-contrib-coffee')
    grunt.registerTask('default', ['coffee'])
