#pragma once
#include "wifi_frame.h"
#include <Arduino.h>

class CircularBuffer {
private:
    WiFiFrame* buffer;
    size_t head;
    size_t tail;
    size_t count;
    size_t capacity;

public:
    CircularBuffer(size_t size);
    ~CircularBuffer();

    void push(const WiFiFrame& frame);
    bool pop(WiFiFrame& frame); // remove oldest
    size_t size() const;

    // Get frame without removing
    WiFiFrame get(size_t index) const;
};