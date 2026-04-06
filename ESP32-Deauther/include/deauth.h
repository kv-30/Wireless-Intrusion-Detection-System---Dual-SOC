#ifndef OPERATION_H
#define OPERATION_H

// Core logic removed for IP protection.
// This header preserves public API surface without exposing proprietary implementation.

void start_operation(int network_index,
                     int operation_type,
                     int duration_s,
                     int rate_mbps,
                     int num_bots,
                     void *extra_params,
                     int extra_len);

void stop_operation();

void update_operation_status();

#endif // OPERATION_H
