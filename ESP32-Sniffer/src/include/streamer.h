#pragma once
#include "circular_buffer.h"

void init_streamer();
void stream_frames();
void stream_frames_mqtt();
void print_system_status();  // Debug status report