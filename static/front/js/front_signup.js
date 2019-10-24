$(function(){
    $('#captcha-img').click(function (event) {
        var self = $(this);
        var src = self.attr('src');
        var newsrc = bbsparam.setParam(src,'xx',Math.random());
        self.attr('src',newsrc);
    });
});