$(document).ready(function () {
    $.fn.hideText = function (nLines) {
        var lht = parseInt($(this).css('lineHeight'))
        for (i = 0; i < $(this).length; i++) {
            self.fullHeight = $(this)[i].offsetHeight
            var lines = ($(this)[i].offsetHeight) / lht
            $(this)[i].fullText = $(this)[i].textContent
            $(this)[i].hiddenText = ''
            if (lines > 2) {
                for (j = 0; j < $(this)[i].fullText.length; j++) {
                    lines = ($(this)[i].offsetHeight) / lht
                    if (lines > nLines) {
                        for (k = $(this)[i].textContent.length - 1; k != 0; k--) {
                            if ($(this)[i].textContent[k] != '.') {
                                $(this)[i].hiddenText = $(this)[i].textContent[k] + $(this)[i].hiddenText
                                $(this)[i].textContent = $(this)[i].textContent.substring(0, k)
                                break
                            }
                        }
                    }
                    if (lines == nLines) {
                        if ($(this)[i].textContent.substring($(this)[i].textContent.length - 3, $(this)[i].textContent.length) != "...") {
                            $(this)[i].textContent += '.'
                        }
                    }
                }
            }
            $(this)[i].hiddenText = $(this)[i].textContent
        }
    }
    $.fn.showText = function () {
        $(this).textContent = $(this).fullText
    }
    $(".card-title").hideText(2)
    $(".card-text").hideText(3)
    $(".card").on('mouseleave', function () {
        $($($(this)[0]).find('.card-title')).hideText(2)
        $($($(this)[0]).find('.card-text')).hideText(3)
    })
    $(".card").on('mouseenter', function () {
        $($(this)[0]).find('.card-title')[0].textContent = $($(this)[0]).find('.card-title')[0].fullText
        $($(this)[0]).find('.card-text')[0].textContent = $($(this)[0]).find('.card-text')[0].fullText
    })
})

