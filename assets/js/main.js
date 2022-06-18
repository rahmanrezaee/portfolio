!function (r) {
    "use strict"; var i = r("body");
    function s() {
        var a = r("#page-ajax-loaded");
        function t() { a.removeClass("fadeOutLeft closed"), a.show(), r("body").addClass("ajax-page-visible") }
        var o = r(".ajax-page-load").each(function () { if (o = r(this).attr("href"), location.hash == location.hash.split("/")[0] + "/" + o.substr(0, o.length - 5)) { var e = r(this).attr("href"); return t(), a.load(e), !1 } }); r(document).on("click", "#ajax-page-close-button", function (e) { e.preventDefault(), r("#page-ajax-loaded").addClass("fadeOutLeft closed"), r("body").removeClass("ajax-page-visible"), setTimeout(function () { r("#page-ajax-loaded.closed").html(""), a.hide() }, 500), location.hash = location.hash.split("/")[0] }).on("click", ".ajax-page-load", function () { var e = location.hash.split("/")[0] + "/" + r(this).attr("href").substr(0, r(this).attr("href").length - 5); return location.hash = e, t(), !1 })
    } function d() { 150 < r(i).scrollTop() ? r(".lmpixels-scroll-to-top").removeClass("hidden-btn") : r(".lmpixels-scroll-to-top").addClass("hidden-btn") } r(function () { r("#contact_form"), r("#contact_form").on("submit", function (e) { if (!e.isDefaultPrevented()) { return r.ajax({ type: "POST", url: "contact_form/contact_form.php", data: r(this).serialize(), success: function (e) { var a = "alert-" + e.type, t = e.message, o = '<div class="alert ' + a + ' alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button>' + t + "</div>"; a && t && (r("#contact_form").find(".messages").html(o), r("#contact_form")[0].reset()) } }), !1 } }) }), r(window).on("load", function () {
        var e, a, t; r(".preloader").fadeOut(800, "linear"), e = r(window).width(), a = "", t = r("#page_container").attr("data-animation"), (a = r(991 < e ? ".page-container" : ".site-main")).addClass("animated " + t), r(".page-scroll").addClass("add-prespective"), a.addClass("transform3d"),
            setTimeout(function () { r(".page-scroll").removeClass("add-prespective"), a.removeClass("transform3d") }, 1e3)
    }).on("hashchange", function (e) { location.hash && s() }),
        r(document).on("ready", function () {
            var l = 15 / r(document).height(), n = 15 / r(document).width();
            r("body").on("mousemove", function (e) {
                var a = e.pageX - r(document).width() / 2, t = e.pageY - r(document).height() / 2, o = n * a * -1, i = l * t * -1; if (r(".page-container").hasClass("bg-move-effect"))
                    var s = r(".home-photo .hp-inner:not(.without-move), .lm-animated-bg"); else s = r(".home-photo .hp-inner:not(.without-move)");
                s.addClass("transition"), s.css({ "background-position": "calc( 50% + " + o + "px ) calc( 50% + " + i + "px )" }),
                    setTimeout(function () { s.removeClass("transition") }, 300)
            }).scroll(function () { d() }); var e = r(".portfolio-grid")

          

        });
}(jQuery);