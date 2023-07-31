# def update():
#     if is_running.get():
#         button_text.set("STOP")
#         current_break_time.set(0)
#         main_time.set(main_time.get() + 1)
#         seconds = main_time.get()
#         main_timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
#     else:
#         button_text.set("START")
#         current_break_time.set(current_break_time.get() + 1)
#         seconds = current_break_time.get()
#         current_break_timer.set(f"{seconds // 3600}:{seconds // 60 % 60 :02d}:{seconds % 60 :02d}")
#         break_time.set(break_time.get() + 1)
#         break_seconds = break_time.get()
#         break_timer.set(f"{break_seconds // 3600}:{break_seconds // 60 % 60 :02d}:{break_seconds % 60 :02d}")
#     window.after(1000, update)