var typed = new Typed('#typed', {
    strings: ['Ask Doctor Python to fix your code...'],
    typeSpeed: 70,
    startDelay: 300,
    showCursor: false,
    onComplete: function () {
        document.getElementsByClassName('ace_text-input')[0].focus();
    }
});