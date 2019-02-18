$(document).ready(function(){
    $('.bxslider').bxSlider({
        minSlides: 4,
        maxSlides: 4,
        slideWidth: 240,
        controls: false
    });

    $(':checkbox').checkboxpicker();

    $('#datetimepicker').datetimepicker({
        viewMode: 'years',
        format: 'YYYY-mm-DD'
    });

    $('#userTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show')
    });

    $(document).on('click', '#add_content_type', function(e){
        e.preventDefault();
        var el = $(this);

        $.ajax({
            url: '/materials/add_content_type/',
            type: 'POST',
            cache: false,
            data: 'model_name=' + el.attr('data-model'),
            success: function(data) {
                if (data.success == true) {
                    var html = '<select class="form-control" data-name-field="' + el.attr('data-name-field') + '" id="' + el.attr('data-model') + '">';

                    $(data.objects).each(function() {
                        html += '<option value="' + $(this).attr('pk') + '">' + $(this).attr('title') + '</option>';
                    });

                    html += '</select>  ';
                    el.before(html);
                    el.attr('id', 'set_select_obj')
                }
            }
        })
    });

    $(document).on('click', '#set_select_obj', function(e) {
        e.preventDefault();
        var el = $(this);
        var repeat_button = false;
        var select = el.parent().find('select');

        el.parent().find('input[name=' + select.attr('data-name-field') + ']').each(function() {
            if (select.val() == $(this).val()) {
                repeat_button = true;
            }
        });

        if (repeat_button == false) {
            var text = $('#' + select.attr('id') + ' :selected').text()

            var html = '<button class="btn btn-primary btn-xs block" onclick="$(this).remove()">' +
                '<input name="' + select.attr('data-name-field') + '" type="hidden" value="' + select.val() + '">' +
                text + ' <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>' +
                '</button>';
            el.before(html);
            select.remove();
            el.attr('id', 'add_content_type');
        }
    });

    $(document).on('click', '.user_add_item', function(e) {
        e.preventDefault();
        var el = $(this);

        $.ajax({
            url: '/materials/put_item/',
            type: 'POST',
            cache: false,
            data: 'item_pk=' + $(this).attr('data-pk') + '&type_btn=' + $(this).attr('data-btn-type')
        })
            .done(function(data) {
                if (data.success == true) {
                    el.text(data.text);
                    el.removeClass('user_add_item');
                    el.addClass('user_del_item');
                }
            })
    });

    $(document).on('click', '.user_del_item', function(e) {
        e.preventDefault();
        var el = $(this);

        $.ajax({
            url: '/materials/del_item/',
            type: 'POST',
            cache: false,
            data: 'item_pk=' + el.attr('data-pk') + '&type_btn=' + el.attr('data-btn-type')
        })
            .done(function(data) {
                if (data.success == true) {
                    el.text(data.text);
                    el.removeClass('user_del_item');
                    el.addClass('user_add_item');
                }
            })
    });

    $(document).on('click', '#cancel_vote', function(e){
        e.preventDefault();
        var el = $(this);

        $.ajax({
            url: '/materials/cancel_vote/',
            type: 'POST',
            cache: false,
            data: 'item_pk=' + el.attr('data-pk') + '&type_btn=' + el.attr('data-type-btn'),
            success: function(data) {
                if (data.success == true) {
                    if (el.attr('data-type-btn') == 1) {
                        $('#like').text(data.number);
                    } else if (el.attr('data-type-btn') == 0) {
                        $('#not_like').text(data.number);
                    }

                    var html = '<a class="btn btn-success btn-xs" id="vote" data-type-btn="1" data-pk="' + el.attr('data-pk') + '">Нравиться</a>' +
                        ' <a class="btn btn-danger btn-xs" id="vote" data-type-btn="0" data-pk="' + el.attr('data-pk') + '">Не нравиться</a>';
                    el.parent().parent().html(html);
                }
            }
        });
    });

    $(document).on('click', '#vote', function (e) {
        e.preventDefault();
        var el = $(this);

        $.ajax({
            url: '/materials/vote/',
            type: 'POST',
            cache: false,
            data: 'item_pk=' + el.attr('data-pk') + '&type_btn=' + el.attr('data-type-btn'),
            success: function(data) {
                if (data.success == true) {
                    if (el.attr('data-type-btn') == 1) {
                        $('#like').text(data.number);
                    } else if (el.attr('data-type-btn') == 0) {
                        $('#not_like').text(data.number);
                    }

                    var btn = '<div class="cancel_vote';
                    if (el.attr('data-type-btn') == 1) {
                        btn += ' green';
                    } else if ((el.attr('data-type-btn') == 0)) {
                        btn += ' red';
                    }

                    btn += '">Ваша оценка ';

                    if (el.attr('data-type-btn') == 1) {
                        btn += '+';
                    } else if ((el.attr('data-type-btn') == 0)) {
                        btn += '-';
                    }

                    btn += '1 <a href="#" id="cancel_vote" data-type-btn="' + el.attr('data-type-btn') + '" data-pk="' + el.attr('data-pk') + '" role="button">отмена</a></div>';
                    el.parent().html(btn);
                }
            }
        });
    });

    var Autocomplete = function(options) {
        this.form_selector = options.form_selector;
        this.url = options.url || '/search/autocomplete/';
        this.delay = parseInt(options.delay || 300);
        this.minimum_length = parseInt(options.minimum_length || 3);
        this.form_elem = null;
        this.query_box = null
    };

    Autocomplete.prototype.setup = function() {
        var self = this;

        this.form_elem = $(this.form_selector);
        this.query_box = this.form_elem.find('input[name=q]');

        // Watch the input box.
        this.query_box.on('keyup', function() {
            var query = self.query_box.val();

            if(query.length < self.minimum_length) {
                return false
            }

            self.fetch(query)
        });

        // On selecting a result, populate the search field.
        this.form_elem.on('click', '.ac-result', function(ev) {
            self.query_box.val($(this).text());
            $('.ac-results').remove();
            return false
        })
    };

    Autocomplete.prototype.fetch = function(query) {
        var self = this;

        $.ajax({
            url: this.url
            , data: {
                'q': query
            }
            , success: function(data) {
                self.show_results(data)
            }
        })
    }

    Autocomplete.prototype.show_results = function(data) {
        // Remove any existing results.
        $('.ac-results').remove();

        var results = data.results || [];
        var results_wrapper = $('<div class="ac-results"></div>');
        var base_elem = $('<div class="result-wrapper"><a href="#" class="ac-result"></a></div>');

        if(results.length > 0) {
            for(var res_offset in results) {
                var elem = base_elem.clone();
                var obj = results[res_offset];
                // Don't use .html(...) here, as you open yourself to XSS.
                // Really, you should use some form of templating.
                elem.find('.ac-result').text(obj);
                console.log(obj.countries);

                var html;
                html =  '<a href="';
                html += obj.href + '" class="block item-search">';
                html += '<div class="row">';
                html += '   <div class="col-md-7">';
                html += '       <img class="img-responsive shadow" title="' + obj.title + '" alt="' + obj.title + '" src="' + obj.main_image + '" >';
                html += '   </div>';
                html += '   <div class="col-md-17">';
                html += '       <div class="title">' + obj.title + ' &bull; <span class="year">' + obj.year_release + '</span></div>';
                html += '       <span class="label label-default">' + obj.main_group_title + '</span>';

                if (obj.genres) {
                    html += '   <span>' + obj.genres + '</span>';
                }

                if (obj.countries) {
                    html += '   <div>' + obj.countries + '</div>';
                }

                html += '   </div>';
                html += ' </div>';
                html += '</a>';
                html += '<div role="separator" class="divider"></div>';
                results_wrapper.append(html)
            }
        } else {
            var elem = base_elem.clone();
            elem.text("No results found.");
            results_wrapper.append(elem)
        }

        this.query_box.after(results_wrapper)
    };

    window.autocomplete = new Autocomplete({
        form_selector: '.autocomplete-me'
    });
    window.autocomplete.setup()


    //var module = angular.module('Cabinet', [], function ($interpolateProvider) {
    //    $interpolateProvider.startSymbol('[[');
    //    $interpolateProvider.endSymbol(']]');
    //}).
    //    config(function($httpProvider){
    //        $httpProvider.defaults.headers.common['X-CSRFToken'] = '{{ csrf_token }}';
    //    });

    var csrftoken = $.cookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});