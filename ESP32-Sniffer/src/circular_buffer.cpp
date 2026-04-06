#include "circular_buffer.h"

CircularBuffer::CircularBuffer(size_t size)
    : head(0), tail(0), count(0), capacity(size)
{
    buffer = new WiFiFrame[size];
}

CircularBuffer::~CircularBuffer() {
    delete[] buffer;
}

void CircularBuffer::push(const WiFiFrame& frame) {
    buffer[head] = frame;
    head = (head + 1) % capacity;
    if (count < capacity) count++;
    else tail = (tail + 1) % capacity;
}

bool CircularBuffer::pop(WiFiFrame& frame) {
    if (count == 0) return false;
    frame = buffer[tail];
    tail = (tail + 1) % capacity;
    count--;
    return true;
}

size_t CircularBuffer::size() const {
    return count;
}

WiFiFrame CircularBuffer::get(size_t index) const {
    if(index >= count) return buffer[tail]; // fallback
    size_t idx = (tail + index) % capacity;
    return buffer[idx];
}