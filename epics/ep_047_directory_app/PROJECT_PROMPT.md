# Project Prompt: Business Activation Directory Platform

> Source brief, stored verbatim. Captured 2026-07-23.

## Objective

Build a production-ready Business Directory platform that acts as the foundation of a Business Activation Engine.

This is not a traditional business directory.

The directory is the operational platform used to discover businesses, manage their lifecycle, activate services, and ultimately convert them into subscribers.

The system must be designed to comfortably scale from a few hundred businesses to hundreds of thousands without architectural redesign.

The platform is expected to become the central operational system for managing every business from discovery through to becoming an active subscriber.

## Primary Objectives

The system must:

- Import businesses from CSV files
- Support future JSON imports
- Support future API imports
- Store businesses in a database (Render PostgreSQL preferred)
- Present businesses through a modern searchable directory
- Track every business through a configurable activation pipeline
- Provide a complete administration control centre
- Be fully mobile responsive
- Be production ready

This is NOT a prototype. Everything should be deployable.

## Technology

**Preferred stack**

Frontend
- React
- NextJS preferred
- TailwindCSS
- TypeScript

Backend
- Node
- Express or NextJS API

Database
- PostgreSQL (Render)

Ingestion modes
- Temporary mode: CSV
- Future: JSON
- Future: API ingestion

## Data Import

Initially data arrives as CSV.

The importer must:

- validate columns
- detect duplicates
- detect missing fields
- detect invalid email
- detect invalid website
- detect malformed phone numbers
- assign category
- assign unique business id
- create timestamps
- create lifecycle status

CSV importer should support:

- Drag & Drop
- Progress Bar
- Error Report
- Import Summary
- Rollback

## Business Record

Each business should have a permanent unique identifier.

Example: `TP-PLUMB-000001`

Never changes. Everything references this identifier.

Store:

- Business Name
- Trading Name
- Category
- Sub Category
- Owner (future)
- Email
- Phone
- Mobile
- Website
- Facebook
- Instagram
- LinkedIn
- Address
- Town
- County
- Postcode
- Latitude
- Longitude
- Google Rating
- Review Count
- Opening Hours
- Description
- Imported Source
- Import Date
- Last Updated
- Status
- Notes
- Tags
- Internal Notes

## Traditional Directory Features

Homepage
- Categories
- Sub Categories
- Town listings
- County listings
- Alphabetical listings
- Newest businesses
- Recently updated
- Featured businesses

Search
- Keyword search
- Location search
- Category search
- Radius search
- A-Z index

Business Profile Page
- Photos
- Map
- Contact details
- Opening hours
- Description
- Services
- Website
- Social links
- Reviews placeholder
- Claim Business button
- Related businesses
- Nearby businesses
- Breadcrumb navigation
- SEO metadata
- Schema.org support
- Pagination
- Filtering
- Sorting
- Responsive design

## Directory Search

Search by:

- Business Name
- Category
- Sub Category
- Town
- County
- Postcode
- Services
- Keywords
- Phone
- Email
- Business ID
- Status
- Tags

## Administration Console

This is the heart of the platform. It is NOT just an admin screen. It is an operational control centre.

Dashboard must show:

- Businesses imported
- Businesses active
- Businesses claimed
- Businesses published
- AI activated
- Subscribers
- Categories
- Imports today
- Imports this week
- Imports this month
- Pipeline health
- Conversion percentages
- Error count
- Duplicate count
- Missing email
- Missing phone
- Missing website
- Businesses awaiting action
- Businesses stalled
- Average pipeline duration
- Recent activity

## Pipeline Management

Every business has a lifecycle. Pipeline should be configurable.

Default pipeline:

1. Discovered
2. Imported
3. Validated
4. Categorised
5. Directory Published
6. Verification Email Pending
7. Verification Sent
8. Verification Opened
9. Verification Completed
10. Business Claimed
11. Website Generated
12. Website Viewed
13. Website Ready
14. Publish Requested
15. Website Published
16. AI Assistant Available
17. AI Assistant Activated
18. Lead Received
19. Customer Contacted
20. Subscriber
21. Cancelled
22. Archived

Every transition must be timestamped. Never overwrite history. Store complete audit trail.

## Pipeline Dashboard

Visual Kanban style.

Columns:
- Discovered
- Imported
- Validated
- Verification
- Claimed
- Website
- Published
- Subscriber

Each column shows:
- Count
- Movement today
- Average time
- Blocked items

Users can:
- Filter
- Search
- Drag if manual
- Bulk update
- Open business
- View history

## Business Timeline

Every business has a timeline.

Example:

```
Imported
  ↓
Validated
  ↓
Verification Sent
  ↓
Email Opened
  ↓
Claimed
  ↓
Website Generated
  ↓
Viewed
  ↓
Published
  ↓
AI Activated
  ↓
Subscriber
```

Every event has:
- Timestamp
- User
- Source
- Action
- Notes

## Analytics Dashboard

Charts:

- Businesses imported/day
- Verification rate
- Claim rate
- Publish rate
- Activation rate
- Subscriber growth
- Category performance
- Geographical distribution
- Import sources
- Conversion funnel
- Pipeline velocity
- Average time per stage

## Event Logging

Everything should generate events.

Examples:
- Business imported
- Email sent
- Email opened
- Link clicked
- Website viewed
- Publish clicked
- AI enabled
- Lead captured
- Call scheduled
- Subscription started

Every event stored permanently. Do not aggregate. Store raw events.

## Audit System

Every change:
- Who
- When
- Old value
- New value
- Reason

Never lose history.

## Dashboard Widgets

- Today's imports
- Pipeline
- Recent activity
- Businesses needing attention
- Failed imports
- Verification queue
- Claims awaiting approval
- Website publishing queue
- New subscribers
- Latest leads
- System health

## Notification Centre

Admin notifications:

- Failed import
- Duplicate detected
- Verification bounced
- Business claimed
- Website published
- Lead received
- Subscription started
- Errors
- Warnings
- Information

## User Roles

- Super Admin
- Admin
- Sales
- Operations
- Support
- Read Only
- Future: Business Owner

## Future Modules

- Website Generator
- AI Assistant
- CRM
- Email campaigns
- SMS campaigns
- Payments
- Subscriptions
- Customer Portal
- Knowledge Base
- Analytics AI
- Recommendation Engine
- Lead Scoring
- Marketing Automation

## Design Philosophy

This is NOT merely a directory. It is a Business Activation Platform. The directory is simply the first touchpoint.

Every screen should answer one question:

> "What is the next action required to move this business further through the activation pipeline?"

The administration console is the operational control centre for the entire business lifecycle.

Every feature should reduce friction. Every screen should improve operational efficiency. Every business should have a clear current state, complete history, and obvious next action.

The system should feel less like Yellow Pages and more like an air traffic control system for thousands of businesses moving continuously through an activation pipeline.

Build for production. Build for scale. Build for automation.

Everything should be measurable. Everything should be searchable. Everything should be auditable. Everything should be extensible.

The objective is not to build a directory. The objective is to build the operating system for acquiring, activating, and managing businesses at scale.
