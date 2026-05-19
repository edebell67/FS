# P&L Graph Performance Optimization

**Date:** 2026-01-13  
**Time:** 22:01  
**Issue:** P&L Graph page appeared frozen/non-responsive when loading dates with large datasets

---

## Problem Description

The P&L Graph page was slow to render when selecting newer dates with more trade data. The chart appeared to "not work" but was actually just loading very slowly due to:

1. Using `category` scale which creates a label for every unique timestamp
2. No data decimation to reduce rendered points
3. Missing date adapter for efficient time-based parsing

---

## Changes Made

### 1. `pnl_graph.html`

- [x] Added `chartjs-adapter-date-fns` script (required for time scale)

```html
<!-- 2026-01-13: Added date adapter for time scale performance optimization -->
<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
```

---

### 2. `pnl_graph.js`

- [x] Added decimation plugin configuration (lines 1304-1309)
  - Algorithm: `lttb` (Largest Triangle Three Buckets) - preserves visual shape
  - Samples: 500 max points to display

```javascript
// 2026-01-13: Added decimation for performance with large datasets
decimation: {
    enabled: true,
    algorithm: 'lttb',
    samples: 500
},
```

- [x] Changed x-axis from `category` to `time` scale (lines 1367-1385)
  - More efficient for time-series data
  - Native date parsing instead of string labels
  - Automatic tick distribution

```javascript
// 2026-01-13: Switched to 'time' scale for better performance with large datasets
scales: {
    x: {
        type: 'time',
        display: true,
        time: {
            unit: 'minute',
            displayFormats: {
                minute: 'HH:mm',
                hour: 'HH:mm'
            },
            tooltipFormat: 'HH:mm:ss'
        },
        ...
    }
}
```

---

## Verification

- [ ] Hard refresh page (`Ctrl + Shift + R`)
- [ ] Select date with large dataset
- [ ] Confirm chart renders quickly
- [ ] Verify visual accuracy of chart lines

---

## Notes

- Console errors about "Bardeen" are from a browser extension, not this code
- If further optimization is needed, consider adding a loading spinner during data fetch
