# TASK: Enhance Manual Booking (Calendar Date Picker)

## 1. Problem Description
The current manual booking system (Schedule tab) only prompts for a Title and defaults to "Current Time". It needs a proper date/time selection.

## 2. Requirements
- [ ] Implement a Date/Time picker for New Bookings.
- [ ] Allow selection of duration or End Time.
- [ ] Link to Client list for easy counterparty assignment.

## 3. Implementation Plan
- [ ] **Step 1: UI Update**
  - Replace the `window.prompt` in `renderCalendar()` with a structured form.
  - Use `<input type="datetime-local">` for mobile-native date picking.
- [ ] **Step 2: State Sync**
  - Update `POST /api/v1/calendar` payload to include the user-selected date.

## 4. Log
- 2026-02-24: Feature request from user during device testing.
