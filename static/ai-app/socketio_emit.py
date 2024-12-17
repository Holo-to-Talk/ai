from socketio_Config import socketio

def socketio_emit_flag_enter():
    socketio.emit('update_flag_enter', {})

def socketio_emit_flag_enter2():
    socketio.emit('update_flag_enter2', {})

def socketio_emit_flag_space():
    socketio.emit('update_flag_space', {})

def socketio_emit_telop(telopContent):
    socketio.emit('update_telop', {'telop': telopContent})

def socketio_emit_telop_reset():
    socketio.emit('update_telop', {'telop': ""})

def socketio_emit_telop_add_display_none():
    socketio.emit('update_telop_add_display_none', {})

def socketio_emit_telop_remove_display_none():
    socketio.emit('update_telop_remove_display_none', {})

def socketio_emit_input(inputContent):
    socketio.emit('update_input', {'input': inputContent})

def socketio_emit_output(outputContent):
    socketio.emit('update_output', {'output': outputContent})

def socketio_emit_output_reset():
    socketio.emit('update_output', {'output': ""})

def socketio_emit_countdown(countdown):
    socketio.emit('update_countdown', {'countdown': countdown})

def socketio_emit_countdown_reset():
    socketio.emit('update_countdown', {'countdown': ""})

def socketio_emit_start_switching():
    socketio.emit('start_switching', {})

def socketio_emit_stop_switching():
    socketio.emit('stop_switching', {})

def socketio_emit_image_qr_add_active():
    socketio.emit('image_qr_add_active', {})

def socketio_emit_image_qr_remove_active():
    socketio.emit('image_qr_remove_active', {})

def socketio_emit_start_telop_animation():
    socketio.emit('start_telop_animation', {})

def socketio_emit_stop_telop_animation():
    socketio.emit('stop_telop_animation', {})