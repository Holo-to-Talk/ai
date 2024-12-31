const socket = io()

// 画像切替秒数（1 => 0.001s）
const switchImageIntervalTime = 1;
// テロップ切替秒数（400 => 0.4s）
const telopAnimationIntervalTime = 400;
// テロップ設定
const dotsLength = 3;
// Enter用Flag
let flag_enter = false;
// Enter用Flag
let flag_enter2 = false;
// Space用Flag
let flag_space = false;

// キーが押されたら
document.addEventListener('keydown', function(event) {
    // False False Falseなら
    if (!flag_enter && !flag_space && !flag_enter2) {
        // Enterが押されたら
        if (event.key === 'Enter') {
            // メイン処理始動
            socket.emit('enter_starting')
        }
    // True False Falseなら
    }else if (flag_enter && !flag_space && !flag_enter2) {
        // Spaceが押されたら
        if (event.key === ' ') {
            // Flag変更
            socket.emit('space_phone')
        }
    // True True False
    }else if (flag_enter && flag_space && !flag_enter2) {
        // Enterが押されたら
        if (event.key === 'Enter') {
            // Flag変更
            socket.emit('enter_conversation')
        }
    }
});

// FLag変更
socket.on('update_flag_enter', () => {
    if (flag_enter) {
        flag_enter = false;
    }else {
        flag_enter = true;
    }
});

// Flag変更
socket.on('update_flag_enter2', () => {
    if (flag_enter2) {
        flag_enter2 = false;
    }else {
        flag_enter2 = true;
    }
});

// Flag変更
socket.on('update_flag_space', () => {
    if (flag_space) {
        flag_space = false;
    }else {
        flag_space = true;
    }
});

// テロップ変更
socket.on('update_telop', (data) => {
    document.getElementById('telop').textContent = data.telop;
});

// テキスト変更
socket.on('update_input', (data) => {
    document.getElementById('input').textContent = data.input;
});

// テキスト変更
socket.on('update_output', (data) => {
    document.getElementById('output').textContent = data.output;
});

// カウント変更
socket.on('update_countdown', (data) => {
    document.getElementById('countdown').textContent = data.countdown;
});

// テロップ削除
socket.on('update_telop_add_display_none', () => {
    document.getElementById('div_telop').classList.add('display_none');
});

// テロップ表示
socket.on('update_telop_remove_display_none', () => {
    document.getElementById('div_telop').classList.remove('display_none');
});

// img取得
const images = document.querySelectorAll('#div_img img');
// 表示順序
let sequence = [0, 1, 2, 1];
// 初期位置
let currentIndex = 1;
// IntervalId
let intervalId = null;

// 画像切替
function switchImage() {
    // クラス削除
    images.forEach(img => img.classList.remove('active'));
    // クラス付与
    images[sequence[currentIndex]].classList.add('active');
    // 位置変更
    currentIndex = (currentIndex + 1) % sequence.length;
}

// 画像リセット
function resetImage() {
    // クラス削除
    images.forEach(img => img.classList.remove('active'));
    // クラス付与
    images[sequence[0]].classList.add('active');
}

// 画像切替スタート
socket.on('start_switching', () => {
    if (!intervalId) {
        // IntervalId取得
        intervalId = setInterval(switchImage, switchImageIntervalTime);
    }
});

// 画像切替ストップ
socket.on('stop_switching', () => {
    if (intervalId) {
        // 画像切替ストップ
        clearInterval(intervalId);
        // IntervalId削除
        intervalId = null;
    }
    // 画像リセット
    resetImage();
});

// QRCode表示
socket.on('image_qr_add_active', () => {
    // クラス削除
    images.forEach(img => img.classList.remove('active'));
    // クラス付与
    document.getElementById('image_qr').classList.add('active');
});

// QRCode削除
socket.on('image_qr_remove_active', () => {
    // クラス削除
    images.forEach(img => img.classList.remove('active'));
    // クラス付与
    images[sequence[0]].classList.add('active');
});

// テロップ取得
const telop = document.getElementById('telop');
// テロップ
let dots = "";
// IntervalId
let intervalId2 = null;

// Animation
function startTelopAnimation() {
    // テロップ付与
    dots = dots.length < dotsLength ? dots + "." : "";
    // テキスト変更
    telop.textContent = "録音しています" + dots;
}

// Animationリセット
function resetTelopAnimation() {
    // テロップリセット
    dots = "";
    // テキスト変更
    telop.textContent = "録音が終わりました";
}

// Animationスタート
socket.on('start_telop_animation', () => {
    if (!intervalId2) {
        // IntervalId取得
        intervalId2 = setInterval(startTelopAnimation, telopAnimationIntervalTime);
    }
});

// Animationストップ
socket.on('stop_telop_animation', () => {
    if (intervalId2) {
        // Animationストップ
        clearInterval(intervalId2);
        // IntervalId削除
        intervalId2 = null;
    }
    // Animationリセット
    resetTelopAnimation();
});