(function () {
    window.addEventListener('load', _ => {
        var level = document.querySelector('#id_level')
        var achievement = document.querySelector('#id_achievement')
        var tag = document.querySelector('#id_tag')
        var event_key = document.querySelector('#id_event_key')
        // event_key.disabled = true;
        level.addEventListener('change', _ => {
            process_auto_key(event_key, level, achievement, tag)
        })
        achievement.addEventListener('change', _ => {
            process_auto_key(event_key, level, achievement, tag)
        })
        tag.addEventListener('change', _ => {
            process_auto_key(event_key, level, achievement, tag)
        })  
    })
})()

function process_auto_key(event_key, level, achievement, tag){
    let a = (level.value * 10 + Math.floor(Math.random() * 10)).toString()
    let b = (achievement.value * 10 + Math.floor(Math.random() * 10)).toString()
    let c = (tag.value * 10 + Math.floor(Math.random() * 10)).toString()
    event_key.value = parseInt(a+b+c)
}