"""
Smart Estimation Engine for LaundryFlow
Implements rule-based ready-time calculation factoring in:
- Base service duration
- Current queue load (active orders)
- Outlet operating hours (rollover if past closing time)
- Express priority weighting
"""
from datetime import datetime, timedelta, time

def calculate_estimated_ready_time(service_duration_minutes, is_express=False, active_queue_count=0, current_time=None, opens_at_str="08:00", closes_at_str="21:00"):
    """
    Calculates estimated ready datetime based on service duration, queue overhead,
    and business hours.
    """
    if current_time is None:
        current_time = datetime.now()
    
    # 1. Base duration
    total_minutes = service_duration_minutes
    
    # Express bonus: faster throughput
    if is_express:
        # Express orders jump queue, minimal queue delay
        queue_buffer_minutes = min(active_queue_count * 5, 30)
    else:
        # Standard queue buffer: e.g. 15 minutes per waiting order, capped at 180 mins
        queue_buffer_minutes = min(active_queue_count * 15, 180)
    
    total_minutes += queue_buffer_minutes
    
    # Parse outlet operating hours
    open_hour, open_min = map(int, opens_at_str.split(":"))
    close_hour, close_min = map(int, closes_at_str.split(":"))
    
    # Simulate time advancing through operating windows
    sim_time = current_time
    
    # If currently before opening, jump to open
    daily_open_today = sim_time.replace(hour=open_hour, minute=open_min, second=0, microsecond=0)
    daily_close_today = sim_time.replace(hour=close_hour, minute=close_min, second=0, microsecond=0)
    
    if sim_time < daily_open_today:
        sim_time = daily_open_today
    elif sim_time >= daily_close_today:
        # Jump to next day opening
        sim_time = (daily_open_today + timedelta(days=1))
    
    remaining_work_minutes = total_minutes
    
    while remaining_work_minutes > 0:
        daily_close = sim_time.replace(hour=close_hour, minute=close_min, second=0, microsecond=0)
        minutes_until_close = int((daily_close - sim_time).total_seconds() / 60)
        
        if minutes_until_close <= 0:
            # Move to next day opening
            sim_time = (sim_time + timedelta(days=1)).replace(hour=open_hour, minute=open_min, second=0, microsecond=0)
            continue
            
        if remaining_work_minutes <= minutes_until_close:
            sim_time += timedelta(minutes=remaining_work_minutes)
            remaining_work_minutes = 0
        else:
            remaining_work_minutes -= minutes_until_close
            sim_time = (sim_time + timedelta(days=1)).replace(hour=open_hour, minute=open_min, second=0, microsecond=0)

    # Confidence label based on queue conditions
    if active_queue_count > 10:
        confidence = "Perkiraan Waktu Tinggi (Antrean Padat)"
    elif is_express:
        confidence = "Prioritas Express (Jalur Cepat)"
    else:
        confidence = "Estimasi Cerdas (Kapasitas Normal)"

    return sim_time.strftime("%Y-%m-%d %H:%M"), confidence
