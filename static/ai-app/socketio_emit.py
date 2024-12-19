from socketio_Config import socketio

# Enter用FLag変更
def socketio_emit_flag_enter():
    socketio.emit('update_flag_enter', {})

# Enter用FLag変更
def socketio_emit_flag_enter2():
    socketio.emit('update_flag_enter2', {})

# Space用FLag変更
def socketio_emit_flag_space():
    socketio.emit('update_flag_space', {})

# テロップ変更
def socketio_emit_telop(telopContent):
    socketio.emit('update_telop', {'telop': telopContent})

# テロップリセット
def socketio_emit_telop_reset():
    socketio.emit('update_telop', {'telop': ""})

# テロップ削除
def socketio_emit_telop_add_display_none():
    socketio.emit('update_telop_add_display_none', {})

# テロップ表示
def socketio_emit_telop_remove_display_none():
    socketio.emit('update_telop_remove_display_none', {})

# テキスト変更
def socketio_emit_input(inputContent):
    socketio.emit('update_input', {'input': inputContent})

# テキスト変更
def socketio_emit_output(outputContent):
    socketio.emit('update_output', {'output': outputContent})

# テキストリセット
def socketio_emit_output_reset():
    socketio.emit('update_output', {'output': ""})

# カウント変更
def socketio_emit_countdown(countdown):
    socketio.emit('update_countdown', {'countdown': countdown})

# カウントリセット
def socketio_emit_countdown_reset():
    socketio.emit('update_countdown', {'countdown': ""})

# 画像切替スタート
def socketio_emit_start_switching():
    socketio.emit('start_switching', {})

# 画像切替ストップ
def socketio_emit_stop_switching():
    socketio.emit('stop_switching', {})

# QRCode削除
def socketio_emit_image_qr_add_active():
    socketio.emit('image_qr_add_active', {})

# QRCode表示
def socketio_emit_image_qr_remove_active():
    socketio.emit('image_qr_remove_active', {})

# Animationスタート
def socketio_emit_start_telop_animation():
    socketio.emit('start_telop_animation', {})

# Animationストップ
def socketio_emit_stop_telop_animation():
    socketio.emit('stop_telop_animation', {})