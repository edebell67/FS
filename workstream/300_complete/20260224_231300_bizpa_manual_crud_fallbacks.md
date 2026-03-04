# TASK: Implement Full Manual CRUD & Fallback UI

## 1. Objective
Provide manual "Add/Update" capabilities for all business sections (Receipts, Invoices, Expenses, etc.) to ensure the app remains functional when Voice NLU is unavailable or inaccurate.

## 2. Requirements
- [ ] **Manual Receipt Entry**: Add form for Merchant, Amount, Date, and Label.
- [ ] **Manual Invoice Entry**: Add form for Client, Ref Number, Amount, and Due Date.
- [ ] **Expense Tracking**: Manual input for non-receipted business costs.
- [ ] **Edit Capability**: Allow clicking existing items in the Timeline to update their fields.

## 3. Implementation Plan
- [ ] **Step 1: Universal Modal/Form Container**
  - Create a reusable `renderForm` component in `App.jsx`.
- [ ] **Step 2: Add Buttons**
  - Place a "+" button in the header of each tab (Timeline, Tax).
- [ ] **Step 3: Backend Bindings**
  - Connect forms to existing `POST /api/v1/items` and `PATCH /api/v1/items/:id` routes.

## 4. Maintenance Notes
- Prioritize UI cleaniness over voice for this phase to ensure high app reliability.
