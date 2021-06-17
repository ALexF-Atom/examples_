(function(){
    window.addEventListener('load', _ =>{ 
        var element = document.querySelector('div.fieldBox.field-preview div.readonly')
        if (!element){
            element = document.querySelector('div.form-row.field-preview div.readonly')
        }
        var choise = document.querySelector('.data-choise')
        choise.addEventListener('change', _=>{
            fetch('/backgrounds/' + choise.value).then((response) => {
                return response.json();}).then((data) => {
                    // console.log(element)
                    element.innerHTML = data['value']
                })
        })
    })
})()