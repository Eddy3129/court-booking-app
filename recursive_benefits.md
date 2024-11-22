"""
Benefits of Recursive Search in Court Availability System:

1. Natural Problem Structure:
   - Court availability search naturally branches into two directions:
     a) Searching forward in time (later slots)
     b) Searching backward in time (earlier slots)
   - Recursion naturally matches this tree-like search pattern

2. Elegant Alternative Slot Discovery:
   - When preferred slot isn't available, we want to find:
     * Different courts at the same time
     * Same court at different times
   - Each recursive call can explore both dimensions smoothly

3. Controlled Search Space:
   - Using search_window parameter limits how far we search
   - tried_times set prevents revisiting same slots
   - Base case ensures termination when we've searched enough

4. Memory Efficiency:
   - Only keeps track of successful finds
   - Doesn't need to store entire schedule tree
   - Stack frames naturally maintain search history

5. Easy to Modify:
   - Simple to add new search criteria
   - Can easily adjust search patterns
   - Flexible for adding new features
"""

def check_availability_recursive(court_filter, day, preferred_time, preferred_court, duration, 
                               search_window=2, tried_times=None):
    """
    Recursively check availability and suggest alternatives.
    
    # Step 1: Initialize first call
    if tried_times is None:
        tried_times = set()
        print(f"\nChecking availability for Court {preferred_court} at {preferred_time}...")
    
    # Step 2: Check if we've searched too far (Base Case)
    time_dt = datetime.strptime(preferred_time, "%I:%M %p")
    if any(abs((datetime.strptime(t, "%I:%M %p") - time_dt).total_seconds() / 3600) > search_window 
           for t in tried_times):
        return []
    
    # Step 3: Track checked times
    tried_times.add(preferred_time)
    
    # Step 4: Check current slot
    slots = find_consecutive_slots(court_filter, day, preferred_court, preferred_time, duration)
    results = []
    
    if slots:
        results.append({
            'court': preferred_court,
            'time': preferred_time,
            'slots': slots,
            'type': 'preferred' if preferred_time == slots[0] else 'alternative'
        })
    
    # Step 5: Check alternative courts
    available_courts = [c for c in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] 
                       if c != preferred_court and preferred_time in court_filter.days[day][c]]
    
    for court in available_courts:
        alt_slots = find_consecutive_slots(court_filter, day, court, preferred_time, duration)
        if alt_slots:
            results.append({
                'court': court,
                'time': preferred_time,
                'slots': alt_slots,
                'type': 'alternative'
            })
    
    # Step 6: Recursive calls for next time slots
    next_time_later = (time_dt + timedelta(minutes=30)).strftime("%I:%M %p")
    next_time_earlier = (time_dt - timedelta(minutes=30)).strftime("%I:%M %p")
    
    # Check both later and earlier times recursively
    for next_time in [next_time_later, next_time_earlier]:
        if next_time not in tried_times:
            results.extend(check_availability_recursive(
                court_filter, day, next_time, preferred_court, duration, 
                search_window, tried_times))
    
    return results
    """
    pass  # Commented out for explanation

"""
Alternative Non-Recursive Approach Would Need:

1. Multiple nested loops:
   - Loop through time window
   - Loop through courts
   - Loop through time slots
   - Loop for consecutive slots

2. Complex state management:
   - Track all checked times
   - Maintain separate lists for preferred/alternative
   - Handle boundary conditions manually

3. More complex code organization:
   - Separate functions for forward/backward search
   - Additional helper functions for state management
   - More complex result aggregation

4. Less flexible search patterns:
   - Fixed search order
   - Harder to modify search strategy
   - More difficult to add new search dimensions

Example of why recursive is better:

Non-recursive approach might look like:
```python
def check_availability_iterative(court_filter, day, time, court, duration):
    results = []
    checked_times = set()
    time_dt = datetime.strptime(time, "%I:%M %p")
    
    # Search forward
    current_time = time_dt
    while current_time < time_dt + timedelta(hours=2):
        # Check current time
        # Check other courts
        # Move to next slot
        current_time += timedelta(minutes=30)
    
    # Search backward
    current_time = time_dt
    while current_time > time_dt - timedelta(hours=2):
        # Check current time
        # Check other courts
        # Move to previous slot
        current_time -= timedelta(minutes=30)
        
    return results
```

This iterative approach:
1. Is more complex
2. Harder to maintain
3. Less flexible
4. More prone to errors
5. Harder to modify for new features
"""
