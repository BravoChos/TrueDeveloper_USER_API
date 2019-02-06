import logging.handlers
import threading

class NonBlockingSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        threading.Thread(
            target = super(NonBlockingSMTPHandler, self).emit,
            args   = (record,)
        ).start()
