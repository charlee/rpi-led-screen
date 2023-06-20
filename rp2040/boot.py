import usb_cdc
import storage
import usb_midi


# enable USD data port
usb_cdc.enable(console=True, data=True)

storage.disable_usb_drive()
usb_midi.disable()

