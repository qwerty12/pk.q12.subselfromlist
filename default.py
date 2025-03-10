import xbmc

def wait_for_window(window, attempts=5, wait=5):
    cond = f"Window.IsActive({window})"
    for _ in range(attempts):
        if xbmc.getCondVisibility(cond):
            return True
        xbmc.sleep(wait)

    return False

def main():
    if xbmc.getCondVisibility("!VideoPlayer.HasSubtitles"):
        return

    player = xbmc.Player()
    sub_streams_len = len(player.getAvailableSubtitleStreams())
    if sub_streams_len == 2:
        xbmc.executebuiltin("Action(CycleSubtitle)")
        return
    elif sub_streams_len <= 1: # redundant because of !VideoPlayer.HasSubtitles, I guess
        return

    if not (already_paused := xbmc.getCondVisibility("Player.Paused")):
        player.pause()

    old_subs = player.getSubtitles()
    xbmc.executebuiltin("ActivateWindow(osdsubtitlesettings)")
    if not wait_for_window("osdsubtitlesettings"):
        return

    xbmc.executebuiltin("SetFocus(-178)", wait=True) # Skin.ToggleDebug()
    if xbmc.getInfoLabel("System.CurrentControlID") == "-178":
        xbmc.executebuiltin("Action(select)")
    if not wait_for_window("selectdialog"):
        xbmc.executebuiltin("Action(down)")
        xbmc.executebuiltin("Action(down)")
        xbmc.executebuiltin("Action(down)")
        xbmc.executebuiltin("Action(select)")
        if not wait_for_window("selectdialog"):
            return

    while xbmc.getCondVisibility("[Window.IsActive(osdsubtitlesettings) + Window.IsActive(selectdialog)]"):
        xbmc.sleep(500)

    for _ in range(4):
        xbmc.sleep(100)
        if player.getSubtitles() != old_subs:
            break
    xbmc.executebuiltin("Dialog.Close(osdsubtitlesettings, true)")

    if player.getSubtitles() != old_subs:
        player.showSubtitles(True)

    if not already_paused:
        player.pause()

if __name__ == "__main__":
    main()