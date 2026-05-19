# GBP Optimized Strategy Card
**Date**: 2026-05-13
**Optimized for**: GBPAUD_C

## Parameters
| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Conf High** | 20 | Count threshold for high-confidence entries |
| **Conf Med** | 8 | Count threshold for medium-confidence entries |
| **Conf Low** | 3 | Count threshold for low-confidence entries |
| **Bucket Min** | 5 | Time-window for cluster anchoring |
| **Offset** | 0.0 | Price buffer added to entries |
| **TP / SL** | Market | Exit based on pattern rejection logic |

## Performance (Net of -2.0 Pips Cost)
- **Net Pips**: 128.7
- **Pips / Hour**: 17.16
- **Alt-Net**: -212.0
- **Trade Count**: 28

## Notes
- Results are strictly based on **Buy at Ask / Sell at Bid**.
- The strategy shows high consistency with a strongly negative "Alt-Net", confirming a genuine directional edge.
- 5-minute buckets proved to be the most stable filter against noise.
