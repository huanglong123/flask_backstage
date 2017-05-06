$(function(){
    $('#result input[type="checkbox"]').change(function(){
        var code = $(this).val();
        var st = $(this).attr('checked') ? 'true' : 'false';
        var url = '/admin/active/get/'+ code +'/'+ st +'/';
        $.get(url);
    });
    $('#get_all').change(function(){
        var status = $(this).attr('checked') ? true : false;
        var chk = $('#result input[type="checkbox"]')
        chk.attr('checked', status);
        chk.each(function(){
            var code = $(this).val();
            var st = $(this).attr('checked') ? 'true' : 'false';
            var url = '/admin/active/get/'+ code +'/'+ st +'/';
            $.get(url);
        })
    })
});