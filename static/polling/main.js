const user_input = $("#user-input")
const questions_div = $('#replaceable-content')

const endpoint = '/search'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call=function(endpoint, url_catch){
    $.getJSON(endpoint,url_catch)
        .done(response=>{
            questions_div.fadeTo('slow',0).promise().then(()=>{
                questions_div.html(response['html_from_view'])
                questions_div.fadeTo('slow',1)
            })
        })
}

user_input.on('keyup',function(){
    const url_catch={
        q:$(this).val()
    }

    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }

    // setTimeout returns the ID of the function to be executed
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, url_catch)
})