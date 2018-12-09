$('document').ready(function(){
    console.log('hello world');
});

function triggerCustomEvent() {
    console.log('form submitted');

    var email = $('#email').val();
    console.log(email);

    var _hsq = window._hsq = window._hsq || [];
    _hsq.push(["identify", {
        email: email
    }]);
    console.log('Completed push identify event');

    _hsq.push(["trackEvent", {
        id: "Submitted Advocate Form"
    }]);
    console.log('Completed push trackEvent event');
}
