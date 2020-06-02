$(document).ready(function () {
    var nIngregients = 0
    var nInstructions = 0
    $('.textInput').on('focus', fieldCreate)
    $('.textInput').on('blur', fieldDelete)

    function fieldCreate() {
        let $this = $(this)
        let $clone = $this.clone()
        let name = $clone[0].name
        if (name != 'title') {
            let n = name.match(/\d/g)
            n = parseInt(n.join("")) + 1
            name = name.split(n - 1)[0] + n
            if (document.getElementById('id_' + name) == null & n < 30) {
                $clone.val('')
                $clone.attr('name', name)
                $clone.attr('id', 'id_' + name)
                $clone.removeAttr('required')
                $clone.removeClass('is-invalid')
                $clone.appendTo($this.parent())
                $($(this)).off('focus', arguments.callee)
                $clone.on('focus', arguments.callee)
                $clone.on('blur', fieldDelete)
            }
        }
    }

    function fieldDelete() {
        if ($(this)[0].name != 'title' & $(this)[0].value == '') {
            let name = $(this)[0].name
            let thisField = name.match(/\d/g)
            let nCheckField = parseInt(thisField.join("")) + 1
            let fieldName = $(this)[0].name.split(nCheckField - 1)[0]
            let checkObj = document.getElementById('id_' + fieldName + nCheckField)
            while (checkObj) {
                if (checkObj.value !== '') {
                    aux = document.getElementById('id_' + fieldName + thisField)
                    aux.value = checkObj.value
                    checkObj.value = ""
                    thisField++
                }
                nCheckField++
                checkObj = document.getElementById('id_' + fieldName + nCheckField)
            }
            nCheckField--
            let nextCheckObj = document.getElementById('id_' + fieldName + nCheckField)
            nCheckField--
            checkObj = document.getElementById('id_' + fieldName + nCheckField)
            while (checkObj) {
                if (checkObj.value == '' & nextCheckObj.value == '' & nCheckField !== -1) {
                    nextCheckObj.remove()
                    $(checkObj).on('focus', fieldCreate)
                }
                nextCheckObj = document.getElementById('id_' + fieldName + nCheckField)
                nCheckField--
                checkObj = document.getElementById('id_' + fieldName + nCheckField)
            }
        }
    }
})