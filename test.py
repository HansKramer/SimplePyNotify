#! /usr/bin/python
#
# \Author : Hans Kramer
#
# \Date   : 
#


import ctypes
import os
import time


libc = ctypes.cdll.LoadLibrary("libc.so.6")


IN_ACCESS        = 0x00000001
IN_MODIFY        = 0x00000002
IN_ATTRIB        = 0x00000004
IN_CLOSE_WRITE   = 0x00000008
IN_CLOSE_NOWRITE = 0x00000010
IN_CLOSE         = IN_CLOSE_WRITE | IN_CLOSE_NOWRITE
IN_OPEN          = 0x00000020
IN_MOVED_FROM    = 0x00000040
IN_MOVED_TO      = 0x00000080
IN_MOVE          = IN_MOVED_FROM | IN_MOVED_TO
IN_CREATE        = 0x00000100
IN_DELETE        = 0x00000200
IN_DELETE_SELF   = 0x00000400
IN_MOVE_SELF     = 0x00000800


class inotify_event(ctypes.Structure):

    _fields_ = [
         ("wd",     ctypes.c_int),
         ("mask",   ctypes.c_int),
         ("cookie", ctypes.c_int),
         ("len",    ctypes.c_int),
         ("name",   ctypes.c_void_p)
    ]

    def __init__(self, *args, **kw):
        if kw.has_key("raw"):
            print("init in another way")
        else:
            ctypes.Structure.__init__(self, *args)

    def __repr__(self):
         return "{} {} {} {}".format(self.wd, self.mask, self.cookie, self.len)


"""
>>> def multiply(klass):
...     def create_a_bunch():
...         a = klass()
...         b = klass()
...         return [a, b]
...     return create_a_bunch
"""
 

def parse_inotify_event(data):
    return_set = []
    while len(data) > 0:
        dst = inotify_event(0, 0, 0, 0)
        ctypes.memmove(ctypes.pointer(dst), data, 16) 
        if dst.len != 0:
            print("not implemented yet")
        return_set += [dst]
        data = data[16:]
    return return_set
    


if __name__ == "__main__":
    print(libc) 
    ifd = libc.inotify_init()
    print(ifd)
    wd = libc.inotify_add_watch(ifd, ctypes.create_string_buffer("/tmp/hello"), IN_MODIFY|IN_CLOSE)
    print(wd)

    time.sleep(4)

    dst = inotify_event(0,0,0,0)
    while True:
        data   = os.read(ifd, 32) 
        events = parse_inotify_event(data)
        print(events)

#        ctypes.memmove(ctypes.pointer(dst), data, 16) 
#        print(data)
#        print(dst)
#        print(dst.wd)
#        print(dst.mask)
#        print(dst.cookie)
#        print(dst.len)
#        print(dst.name)
