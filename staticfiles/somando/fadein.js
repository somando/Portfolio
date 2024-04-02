let targets = document.getElementsByClassName('section');

var prof_items = document.getElementsByClassName('profile-line').length;

const sleep = (time) => new Promise((r) => setTimeout(r, time));

window.onload = async()=>{
	await sleep(2500 + prof_items * 100);
    var windowHeight = window.innerHeight;
    for (let target of targets) {
        var targetPos = target.getBoundingClientRect().top;
        if (!target.classList.contains('is-show')) {
            if (0 > targetPos - windowHeight) {
                target.classList.add('is-show');
                var animation_wait = target.getElementsByClassName('animation-wait');
                var i = 0;
                var animation_wait_items = animation_wait.length;
                while (animation_wait.length > i) {
                    animation_wait[0].classList.remove('animation-wait');
                }
            	await sleep(1000 + animation_wait_items * 200);
            }
        }
    }
}

window.addEventListener('scroll', function () {
    var scroll = window.scrollY;
    var windowHeight = window.innerHeight;
    for (let target of targets) {
        var targetPos = target.getBoundingClientRect().top + scroll;
        if (!target.classList.contains('is-show')) {
            if (scroll > targetPos - windowHeight) {
                target.classList.add('is-show');
                var animation_wait = target.getElementsByClassName('animation-wait');
                var i = 0;
                while (animation_wait.length > i) {
                    animation_wait[0].classList.remove('animation-wait');
                }
            }
        }
    }
});


function delay_set(class_name, delay = 0, tolerance = 0.1) {

    var elements = document.getElementsByClassName(class_name);

    for (var i = 0; i < elements.length; i++) {
        elements[i].style.animationDelay = String(delay + i * tolerance) + "s";
    }

}
