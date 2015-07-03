$(document).ready(function(){
    $('.bxslider').bxSlider({
        minSlides: 4,
        maxSlides: 4,
        slideWidth: 240,
        controls: false
    });

    $('#userTabs a').click(function (e) {
        e.preventDefault();
        $(this).tab('show')
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