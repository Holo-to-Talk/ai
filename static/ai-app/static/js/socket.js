const socket = io()

// 画像切替秒数（1000 => 1s）
const switchImageIntervalTime = 1;
const telopAnimationIntervalTime = 400;
const dotsLength = 3;
let flag_enter = false;
let flag_enter2 = false;
let flag_space = false;

document.addEventListener('keydown', function(event) {
    if (!flag_enter && !flag_space && !flag_enter2) {
        if (event.key === 'Enter') {
            socket.emit('enter_starting')
        }
    }else if (flag_enter && !flag_space && !flag_enter2) {
        if (event.key === ' ') {
            socket.emit('space_phone')
        }
    }else if (flag_enter && flag_space && !flag_enter2) {
        if (event.key === 'Enter') {
            socket.emit('enter_conversation')
        }
    }
});

socket.on('update_flag_enter', () => {
    if (flag_enter) {
        flag_enter = false;
    }else {
        flag_enter = true;
    }
});

socket.on('update_flag_enter2', () => {
    if (flag_enter2) {
        flag_enter2 = false;
    }else {
        flag_enter2 = true;
    }
});

socket.on('update_flag_space', () => {
    if (flag_space) {
        flag_space = false;
    }else {
        flag_space = true;
    }
});

socket.on('update_telop', (data) => {
    document.getElementById('telop').textContent = data.telop;
});

socket.on('update_input', (data) => {
    document.getElementById('input').textContent = data.input;
});

socket.on('update_output', (data) => {
    document.getElementById('output').textContent = data.output;
});

socket.on('update_countdown', (data) => {
    document.getElementById('countdown').textContent = data.countdown;
});

socket.on('update_telop_add_display_none', () => {
    document.getElementById('div_telop').classList.add('display_none');
});

socket.on('update_telop_remove_display_none', () => {
    document.getElementById('div_telop').classList.remove('display_none');
});

const images = document.querySelectorAll('#div_img img');
let sequence = [0, 1, 2, 1];
let currentIndex = 1;
let intervalId = null;

function switchImage() {
    images.forEach(img => img.classList.remove('active'));
    images[sequence[currentIndex]].classList.add('active');
    currentIndex = (currentIndex + 1) % sequence.length;
}

function resetImage() {
    images.forEach(img => img.classList.remove('active'));
    images[sequence[0]].classList.add('active');
}

socket.on('start_switching', () => {
    if (!intervalId) {
        intervalId = setInterval(switchImage, switchImageIntervalTime);
    }
});

socket.on('stop_switching', () => {
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    resetImage();
});

socket.on('image_qr_add_active', () => {
    images.forEach(img => img.classList.remove('active'));
    document.getElementById('image_qr').classList.add('active');
});

socket.on('image_qr_remove_active', () => {
    images.forEach(img => img.classList.remove('active'));
    images[sequence[0]].classList.add('active');
});

const telop = document.getElementById('telop');
let dots = "";
let intervalId2 = null;

function startTelopAnimation() {
    dots = dots.length < dotsLength ? dots + "." : "";
    telop.textContent = "録音しています" + dots;
}

function resetTelopAnimation() {
    dots = "";
    telop.textContent = "録音が終わりました";
}

socket.on('start_telop_animation', () => {
    if (!intervalId2) {
        intervalId2 = setInterval(startTelopAnimation, telopAnimationIntervalTime);
    }
});

socket.on('stop_telop_animation', () => {
    if (intervalId2) {
        clearInterval(intervalId2);
        intervalId2 = null;
    }
    resetTelopAnimation();
});