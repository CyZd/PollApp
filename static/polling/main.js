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

// Initialize all input of type date
var calendars = bulmaCalendar.attach('[type="date"]', options);

// Loop on each calendar initialized
for(var i = 0; i < calendars.length; i++) {
	// Add listener to date:selected event
	calendars[i].on('select', date => {
		console.log(date);
	});
}

// To access to bulmaCalendar instance of an element
var element = document.querySelector('#my-element');
if (element) {
	// bulmaCalendar instance is available as element.bulmaCalendar
	element.bulmaCalendar.on('select', function(datepicker) {
		console.log(datepicker.data.value());
	});
}