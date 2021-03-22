cdef extern from "tobii.h":
    ctypedef struct tobii_api_t:
        pass

    ctypedef enum tobii_error_t:
        TOBII_ERROR_NO_ERROR

    cdef const char* tobii_error_message( tobii_error_t error )

    ctypedef struct tobii_custom_alloc_t:
        pass

    ctypedef struct tobii_custom_log_t:
        pass

    cdef tobii_error_t tobii_api_create(tobii_api_t** api,
        tobii_custom_alloc_t* custom_alloc, tobii_custom_log_t* custom_log )
    cdef tobii_error_t tobii_api_destroy( tobii_api_t* api )

    ctypedef void (*tobii_device_url_receiver_t)( const char* url, void* user_data )
    cdef tobii_error_t tobii_enumerate_local_device_urls( tobii_api_t* api,
        tobii_device_url_receiver_t receiver, void* user_data )

    ctypedef struct tobii_device_t:
        pass

    cdef tobii_error_t tobii_wait_for_callbacks(int device_count, const tobii_device_t** devices)
    cdef tobii_error_t tobii_device_create( tobii_api_t* api, const char * url, tobii_device_t** device )
    cdef tobii_error_t tobii_device_destroy( tobii_device_t* device )
    cdef tobii_error_t tobii_device_process_callbacks( tobii_device_t* device )
    cdef tobii_error_t tobii_device_clear_callback_buffers( tobii_device_t* device )

    ctypedef enum tobii_validity_t:
        TOBII_VALIDITY_INVALID,
        TOBII_VALIDITY_VALID


cdef extern from "tobii_streams.h":
    ctypedef long long unsigned int int64_t
    ctypedef struct tobii_gaze_point_t:
        int64_t timestamp_us
        tobii_validity_t validity
        float position_xy[ 2 ]
    ctypedef void (*tobii_gaze_point_callback_t)( const tobii_gaze_point_t* gaze_point, void* user_data )

    cdef tobii_error_t tobii_gaze_point_subscribe( tobii_device_t* device,
        tobii_gaze_point_callback_t callback, void* user_data );

    cdef tobii_error_t tobii_gaze_point_unsubscribe( tobii_device_t* device );
