from cpython.ref cimport PyObject

from cstream_engine cimport *


class TobiiError(Exception):
    def __init__(self, ec):
        self.ec = ec
        self.message = tobii_error_message(ec).decode('UTF-8')

    def __str__(self):
        return f'{self.message} ({self.ec})'


cdef void tobii_enumerate_local_device_urls_callback_wrapper(const char *url, void* lst):
    tobii_enumerate_local_device_urls_callback(url.decode('UTF-8'))


cdef class Api:
    cdef tobii_api_t *_c_api

    def __cinit__(self):
        cdef tobii_error_t ec = tobii_api_create(&self._c_api, NULL, NULL)
        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            self._c_api = NULL
            raise TobiiError(ec)

    def __dealloc__(self):
        cdef tobii_error_t ec = tobii_api_destroy(self._c_api)
        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            self._c_api = NULL
            raise TobiiError(ec)
        self._c_api = NULL

    # callback accepts a single string argument
    def enumerate_local_device_urls(self):
        l = []

        def append_string(s):
            l.append(s)

        global tobii_enumerate_local_device_urls_callback
        tobii_enumerate_local_device_urls_callback = append_string

        cdef tobii_error_t ec = tobii_enumerate_local_device_urls(
            self._c_api, &tobii_enumerate_local_device_urls_callback_wrapper, NULL)

        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            self._c_api = NULL
            raise TobiiError(ec)

        return l

    def device_create(self, url):
        d = Device()

        cdef bytes py_url_bytes = url.encode()
        cdef char* c_url_string = py_url_bytes

        print(c_url_string)

        cdef tobii_error_t ec = tobii_device_create(
            self._c_api, c_url_string, &d._c_device)

        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            raise TobiiError(ec)

        return d


cdef void gaze_point_callback_wrapper(const tobii_gaze_point_t* gaze_point, void* user_data):
    gaze_point_callback(gaze_point.position_xy[0], gaze_point.position_xy[1],
        gaze_point.validity, gaze_point.timestamp_us)


cdef class Device:
    cdef tobii_device_t *_c_device
    cdef bint _c_go_on

    def __cinit__(self):
        self._c_device = NULL
        self._c_go_on = 0

    def __dealloc__(self):
        self.gaze_point_unsubscribe()
        cdef tobii_error_t ec = tobii_device_destroy(self._c_device)
        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            self._c_device = NULL
            raise TobiiError(ec)
        self._c_device = NULL

    def clear_callback_buffers(self):
        cdef tobii_error_t ec = tobii_device_clear_callback_buffers(self._c_device)
        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            raise TobiiError(ec)

    # callback with signature f(x_pos, y_pos, timestamp, validity)
    def gaze_point_subscribe(self, callback):
        cdef tobii_error_t ec = tobii_gaze_point_subscribe(
            self._c_device, &gaze_point_callback_wrapper, NULL)

        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            raise TobiiError(ec)

        global gaze_point_callback
        gaze_point_callback = callback

    def gaze_point_unsubscribe(self):
        cdef tobii_error_t ec = tobii_gaze_point_unsubscribe(self._c_device)

        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            raise TobiiError(ec)

    def wait_for_callbacks(self):
        cdef tobii_error_t ec = tobii_wait_for_callbacks(1, &self._c_device)

        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            raise TobiiError(ec)

    def process_callbacks(self):
        cdef tobii_error_t ec = tobii_device_process_callbacks(self._c_device)
        if ec != tobii_error_t.TOBII_ERROR_NO_ERROR:
            raise TobiiError(ec)

    def stop(self):
        self._c_go_on = 0

    def run(self):
        self._c_go_on = 1
        while(self._c_go_on):
            self.wait_for_callbacks()
            self.process_callbacks()