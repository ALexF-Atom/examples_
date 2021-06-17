(function () {
    window.addEventListener('load', _ => {
        let color = document.getElementById('id_colors')
        let vector = document.getElementById('id_vector')
        let reg = /#[a-f0-9]{6}/gi
        let div = document.createElement('div')
        div.classList.add('form-row', 'field-vector')
        div.style.width = '150px'
        div.style.height = '80px'
        color.parentNode.after(div)

        if (color.value.length) {
            let array_colors = color.value.match(reg)
            if (array_colors.length == 1) {
                add_background_color(div, array_colors)
            }
            else if (array_colors.length > 1) {
                add_background_image(div, array_colors, vector)
            }
        }

        color.addEventListener('keyup', e => {
            let array_colors = color.value.match(reg)
            if (array_colors.length == 1) {
                add_background_color(div, array_colors)
            }
            else if (array_colors.length > 1) {
                add_background_image(div, array_colors, vector)
            }
        })

        vector.addEventListener('change', e => {
            let array_colors = color.value.match(reg)
            console.log(vector.value)
            if (array_colors.length > 1) {
                add_background_image(div, array_colors, vector)
            }

        })

    })
}
)()

function add_background_color(div, array_colors) {
    div.style.backgroundImage = null
    div.style.backgroundColor = array_colors[0]
}

function add_background_image(div, array_colors, vector) {
    div.style.backgroundColor = null;
    div.style.backgroundImage = 'linear-gradient(' + vector.value + 'deg,' + array_colors.join() + ')'
}
