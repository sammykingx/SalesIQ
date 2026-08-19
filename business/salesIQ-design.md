# SalesIQ - Design Reference

## 1. Purpose

This document defines the visual and interaction language for the
SalesIQ web application.

The attached desktop and mobile screenshots are the primary visual
reference. SalesIQ should **adopt the design language, hierarchy,
spacing, density, navigation behavior, and responsive philosophy** of
the reference while using SalesIQ's own brand identity, terminology,
data, and workflows.

SalesIQ is a sales recording and financial intelligence product. The
interface should communicate:

> **Know your sales. Grow your business.**

The application should feel like a **premium business tool**, not a
generic accounting spreadsheet.

------------------------------------------------------------------------

# 2. Core Design Principles

## 2.1 Information first

The user should understand the state of their business quickly.

Prioritize:

1.  What happened?
2.  What changed?
3.  What needs attention?
4.  What can I do next?

Do not overwhelm the dashboard with every available metric.

## 2.2 Dark, premium, analytical

Use a dark interface as the primary application theme:

-   Near-black page background
-   Slightly lighter surfaces
-   Subtle borders
-   High-contrast typography
-   Green/teal brand accents
-   Restrained use of secondary accent colors for semantic states

The result should feel sophisticated, calm, and data-focused.

## 2.3 Dense but breathable

The reference uses a relatively information-dense dashboard without
feeling cramped.

Maintain:

-   generous outer page margins
-   consistent card padding
-   clear vertical rhythm
-   strong grouping of related information
-   compact controls
-   enough whitespace around major headings

Avoid oversized empty areas that make the application feel like a
marketing website.

## 2.4 Insights over raw data

SalesIQ should not merely display numbers.

Where useful, explain the number:

-   `↑ 18.4% vs. previous week`
-   `Black T-Shirt — 12 sold`
-   `Saturday — ₦120,000`
-   `₦135,000 outstanding`

The interface should help a business owner interpret their sales.

------------------------------------------------------------------------

# 3. SalesIQ Brand Direction

## Brand

**salesiq**

Use the supplied SalesIQ logo as the primary brand mark.

Do not recreate or redraw the logo in CSS.

The logo contains:

-   Deep navy
-   Green/teal
-   White/neutral background treatment

The application should derive its accent system from these brand colors.

## Brand personality

The interface should feel:

-   Professional
-   Intelligent
-   Modern
-   Trustworthy
-   Approachable
-   Business-oriented
-   Efficient

Avoid:

-   overly playful SaaS styling
-   excessive gradients
-   excessive glassmorphism
-   cartoon-like illustrations
-   loud colors
-   excessive animation

------------------------------------------------------------------------

# 4. Color System

The reference is based around a near-black navy interface with
green/teal accents.

Use CSS variables/design tokens rather than hard-coding colors
throughout components.

Suggested starting palette:

``` css
--background: #0A0C11;
--surface: #13161E;
--surface-raised: #181D27;
--surface-hover: #1D2430;

--border: #272D38;
--border-subtle: #202630;

--text-primary: #F3F5F7;
--text-secondary: #A3ADBC;
--text-muted: #6F7A8B;

--brand: #4DB69D;
--brand-strong: #35A989;
--brand-soft: rgba(77, 182, 157, 0.14);

--success: #35C98A;
--warning: #E9B949;
--danger: #F06A7A;
--info: #4AA8E8;
```

These values are starting design tokens, not a requirement to reproduce
every sampled pixel from the screenshots.

### Color rules

-   Green/teal is the primary action and positive-performance color.
-   Red is reserved for negative changes, refunds, or destructive
    states.
-   Yellow/amber is reserved for warnings and partial/pending states.
-   Blue/purple can distinguish secondary data categories.
-   Never use multiple bright accent colors simply for decoration.
-   Financial numbers should remain highly readable.

------------------------------------------------------------------------

# 5. Typography

Use a modern sans-serif font with strong readability.

Preferred direction:

-   Inter
-   Geist
-   system-ui fallback

### Hierarchy

Page title:

-   Large
-   Bold
-   High contrast

Page subtitle:

-   Medium size
-   Muted
-   Explains the purpose or reporting period

Card title:

-   Medium/semibold
-   High contrast

Metric:

-   Large
-   Bold
-   High contrast

Supporting metric:

-   Smaller
-   Muted

Trend:

-   Compact
-   Green for positive
-   Red for negative
-   Neutral when unchanged

Avoid excessive font sizes. The reference feels polished because
typography has clear hierarchy rather than because everything is
oversized.

------------------------------------------------------------------------

# 6. Application Shell

## Desktop

Use a fixed left sidebar and a top utility bar.

Conceptually:

``` text
┌──────────────┬───────────────────────────────────────────┐
│              │ Top utility/navigation bar                │
│   Sidebar    ├───────────────────────────────────────────┤
│              │                                           │
│              │ Main content                              │
│              │                                           │
│              │                                           │
└──────────────┴───────────────────────────────────────────┘
```

### Sidebar

The sidebar should contain:

-   SalesIQ logo/brand mark
-   Dashboard
-   Invoices
-   Customers
-   Products
-   Reports
-   Settings

Navigation items should use:

-   icon
-   label
-   active state

Active navigation should use a subtle green/teal treatment rather than a
loud solid block.

The sidebar can be collapsed on desktop.

## Top bar

The top bar should contain:

-   menu/collapse control
-   global search
-   language or utility controls if required
-   notifications
-   business/account avatar
-   account menu

Keep the top bar visually quiet.

------------------------------------------------------------------------

# 7. Responsive Navigation

The mobile screenshot establishes an important rule:

**Mobile should not simply be a compressed desktop layout.**

On mobile:

-   hide the desktop sidebar
-   use a compact top bar
-   use a bottom navigation bar
-   keep primary actions accessible
-   stack dashboard sections vertically

Recommended mobile bottom navigation:

-   Home
-   Invoices
-   Customers
-   Products
-   Reports

Settings can be accessed from the account/menu area if space is
constrained.

------------------------------------------------------------------------

# 8. Page Header

Every major page should have a consistent page-header structure.

Example:

``` text
Sales

Here's how your sales are performing — Aug 10 to Aug 16.

[ Last 7 days ▼ ]   [ Export ]   [ + Record sale ]
```

### Rules

-   Page title is prominent.
-   Supporting text explains the context.
-   Filters sit to the right on desktop.
-   Primary action uses the SalesIQ green.
-   On mobile, controls wrap or stack naturally.

------------------------------------------------------------------------

# 9. Dashboard Philosophy

The dashboard is the most important screen in SalesIQ.

Its job is to answer:

> **How did my business perform?**

The dashboard should feel like a short business briefing.

Recommended hierarchy:

``` text
Welcome / period summary
        ↓
Core business metrics
        ↓
Business insights
        ↓
Sales performance
        ↓
Top products / customers
        ↓
Financial summary
        ↓
Recent invoices
```

Do not make every section equally prominent.

------------------------------------------------------------------------

# 10. Dashboard Welcome Card

Use a large contextual card similar to the reference.

Example:

``` text
YOUR BUSINESS LAST WEEK

You made ₦485,000 in net sales
across 32 sales.

Sales are up 18.4% compared with the
previous week.

[ Record new sale ]
```

This is the narrative layer of the dashboard.

It should tell the user what the numbers mean.

------------------------------------------------------------------------

# 11. Core Dashboard Metrics

Use a row of compact metric cards on desktop.

Recommended SalesIQ metrics:

### Net Sales

The value of sales after returns.

### Sales

Number of completed sales/invoices.

### Customers

Number of customers involved in the period or relevant customer count.

### Collected

Amount actually collected from customers.

Possible secondary indicators:

-   percentage change
-   comparison period
-   outstanding amount

Example:

``` text
NET SALES

₦485,000

↑ 18.4% vs. previous week
```

The metric cards should be visually distinct but remain part of the same
design system.

------------------------------------------------------------------------

# 12. Financial Metrics

SalesIQ tracks these separately:

-   Gross Sales
-   Returns
-   Net Sales
-   Collected Amount
-   Outstanding Amount

These should never be visually conflated.

Recommended presentation:

``` text
Financial Summary

Gross Sales             ₦520,000
Returns                  -₦35,000
─────────────────────────────────
Net Sales                ₦485,000

Collected                ₦350,000
Outstanding              ₦135,000
```

Use visual emphasis for Net Sales and clear semantic styling for
Returns.

------------------------------------------------------------------------

# 13. Sales Performance Chart

The reference uses a large analytical card.

SalesIQ should use this pattern for:

-   sales trend
-   revenue trend
-   sales count
-   comparison periods

Example:

``` text
Sales Performance

Net sales vs. previous period

[ Week ] [ Month ] [ Year ]

        graph
```

Charts should be:

-   minimal
-   readable
-   dark-theme compatible
-   clearly labeled
-   interactive where useful
-   accompanied by a concise legend

Avoid charts that require the user to decode them.

------------------------------------------------------------------------

# 14. Business Insights

This should be one of SalesIQ's signature components.

Example:

``` text
Business Insights

↑ Your sales are 18.4% higher than last week.

▣ Black T-Shirt is your best-selling product.

◉ Saturday was your busiest sales day.

₦135,000 remains outstanding from customers.
```

Insights should be generated from actual SalesIQ data.

Do not present generic motivational statements as if they were
analytics.

The component should answer:

> **What should I notice about my business?**

------------------------------------------------------------------------

# 15. Top Products

Show products based on actual sales performance.

Example:

``` text
Top Products

Black T-Shirt       12 sold      ₦180,000
██████████████████████

White T-Shirt        8 sold      ₦120,000
██████████████

Blue Jeans           5 sold      ₦150,000
█████████
```

Possible sorting options:

-   Most sold
-   Highest sales value
-   Most recent

Do not introduce inventory indicators because SalesIQ MVP does not
manage inventory.

------------------------------------------------------------------------

# 16. Recent Invoices

Use a compact list/card pattern.

Example:

``` text
Recent Invoices

INV-1004   Sarah Johnson       ₦35,000   Paid
INV-1003   Michael Okafor      ₦50,000   Partially Paid
INV-1002   Amina Yusuf         ₦28,500   Paid
```

Status styles:

-   Paid → green
-   Partially Paid → amber
-   Pending → neutral/blue
-   Refunded/Returned → red or muted
-   Voided → muted

Provide:

`View all invoices →`

------------------------------------------------------------------------

# 17. Invoice Design

Invoices are an important part of the SalesIQ product and should feel
professional.

An invoice contains:

-   SalesIQ business information
-   Customer information
-   Invoice number
-   Invoice date
-   Line items
-   Quantity
-   Unit price
-   Discount
-   Subtotal
-   VAT/tax
-   Amount due
-   Amount paid
-   Outstanding amount
-   Payment status
-   Amount in words
-   QR code
-   Live invoice URL

The invoice should work well both as:

-   downloadable document
-   public live invoice page

------------------------------------------------------------------------

# 18. Live Invoice Page

The public invoice URL should show the **current state** of the invoice.

The customer should be able to understand:

-   who issued the invoice
-   what was purchased
-   how much was due
-   how much has been paid
-   what remains
-   current status
-   returned/refunded items where applicable

The public page may include a concise transaction history where
appropriate.

The business owner's private interface should expose the complete event
log.

------------------------------------------------------------------------

# 19. Invoice Status

Status must be visually obvious.

Recommended states:

``` text
Draft
Unpaid
Partially Paid
Paid
Partially Returned
Returned
Voided
```

Do not allow users to rewrite historical financial events.

Payment and return activity should be recorded as events.

------------------------------------------------------------------------

# 20. Forms

The main form in SalesIQ is **Record New Sale**.

The form should feel fast.

Recommended structure:

``` text
Record New Sale

Customer
[ Search phone, email or name ]

Items
[ Product ] [ Qty ] [ Price ] [ Total ]
[ Product ] [ Qty ] [ Price ] [ Total ]

+ Add item

Discount
VAT / Tax

Payment
○ Unpaid
○ Partially Paid
○ Paid

Amount paid

────────────────────

Subtotal
Discount
VAT
Amount due
Amount paid
Balance

[ Cancel ] [ Generate Invoice ]
```

Product and customer autocomplete should be central to the experience.

------------------------------------------------------------------------

# 21. Customer Experience

Customers are first-class entities.

Customer screens should show:

-   customer information
-   total purchases
-   number of sales
-   outstanding balance
-   latest purchase
-   invoice history
-   payment history
-   return history

The design should make customer history easy to scan.

------------------------------------------------------------------------

# 22. Product Experience

Products are reusable sales data.

Product screens should show:

-   product name
-   default price
-   sales count
-   sales value
-   recent sales
-   customers who purchased it

Do not add stock quantity or inventory workflows to the MVP.

------------------------------------------------------------------------

# 23. Reports

Reports should use the same visual language as the dashboard but provide
deeper analysis.

Supported periods:

-   Daily
-   Weekly
-   Monthly
-   Quarterly
-   Half-yearly
-   Yearly
-   Custom date range

Reports should cover:

-   Gross sales
-   Returns
-   Net sales
-   Collected amount
-   Outstanding amount
-   Number of sales
-   Average sale
-   Best-selling products
-   Busiest sales days
-   Customer activity

------------------------------------------------------------------------

# 24. Buttons

Primary action:

-   SalesIQ green/teal
-   high contrast text
-   medium/semibold label
-   rounded corners
-   subtle hover elevation

Primary actions include:

-   Record New Sale
-   Generate Invoice
-   Save Product
-   Add Customer

Secondary actions:

-   dark surface
-   subtle border
-   neutral text

Destructive actions:

-   reserved for irreversible or financially significant operations
-   require confirmation where appropriate

------------------------------------------------------------------------

# 25. Cards

Use rounded cards consistently.

Suggested radius:

``` css
--radius-card: 18px;
--radius-control: 10px;
--radius-pill: 999px;
```

Cards should have:

-   dark surface
-   subtle border
-   consistent padding
-   minimal shadow

Avoid excessive nested cards.

A card should exist because it groups information meaningfully.

------------------------------------------------------------------------

# 26. Tables and Lists

Desktop can use tables for:

-   invoices
-   customers
-   products
-   reports

Mobile should transform tables into stacked cards/list rows rather than
forcing horizontal scrolling wherever possible.

Each row should expose the most important information first.

------------------------------------------------------------------------

# 27. Mobile Design Rules

The supplied mobile screenshot should be treated as a primary responsive
reference.

### Mobile priorities

1.  Business performance
2.  Record sale
3.  Important insight
4.  Recent invoices
5.  Detailed analytics

### Mobile layout

Stack sections vertically.

Use full-width cards.

Avoid:

-   multi-column metric grids that become too small
-   tiny chart labels
-   dense desktop tables
-   side-by-side controls that become cramped

### Mobile actions

`Record New Sale` should remain highly visible.

The bottom navigation should remain persistent.

------------------------------------------------------------------------

# 28. Responsive Breakpoints

Use responsive behavior rather than designing a separate unrelated
mobile product.

Suggested breakpoints:

``` text
< 640px      Mobile
640–767px    Large mobile
768–1023px   Tablet
1024–1279px  Desktop
1280px+      Large desktop
```

The exact framework breakpoints may follow the implementation framework,
but the design should preserve the hierarchy above.

------------------------------------------------------------------------

# 29. Icons

Use a consistent outline icon family.

Icons should:

-   have consistent stroke weight
-   remain visually secondary to text
-   use brand/semantic colors only when useful

Suggested icon categories:

-   Dashboard → grid/chart
-   Invoices → document
-   Customers → users
-   Products → package
-   Reports → bar chart
-   Settings → sliders/gear
-   Payment → coins/card
-   Return → undo arrow
-   Insights → lightbulb

Do not mix unrelated icon styles.

------------------------------------------------------------------------

# 30. States

Every important screen should account for:

### Loading

Use restrained skeletons that match the final layout.

### Empty

Explain what the user can do next.

Example:

``` text
No sales yet

Record your first sale to start
building your business insights.

[ Record New Sale ]
```

### Error

Explain the problem in plain language and provide recovery.

### Success

Use concise confirmation with an obvious next action.

Example:

``` text
Invoice created successfully.

[ View Invoice ] [ Download ]
```

------------------------------------------------------------------------

# 31. Interaction Philosophy

SalesIQ should feel fast.

Prefer:

-   autocomplete
-   sensible defaults
-   remembered products
-   remembered customers
-   inline actions
-   contextual menus
-   minimal navigation for common tasks

The most frequent workflow:

``` text
Record sale
→ select customer
→ select product
→ enter quantity
→ confirm payment state
→ generate invoice
```

should require as little friction as possible.

------------------------------------------------------------------------

# 32. Visual Relationship Between Data and Meaning

Use visual hierarchy intentionally.

### Primary

-   Net Sales
-   Amount Due
-   Amount Collected
-   Important business insight

### Secondary

-   Number of sales
-   Customers
-   Products
-   Average sale

### Supporting

-   comparison percentages
-   dates
-   invoice IDs
-   secondary descriptions

Do not give every number the same visual weight.

------------------------------------------------------------------------

# 33. Dashboard Example

The finished SalesIQ dashboard should conceptually read like:

``` text
Good morning, Sarah

Here's how your business performed last week.

┌─────────────────────────────────────────────────────────┐
│ Net Sales       Sales       Customers       Collected   │
│ ₦485,000        32          28              ₦350,000    │
│ ↑18.4%          ↑12.5%      ↑10.7%          72%         │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Business Insights                                       │
│ ↑ Sales are 18.4% higher than last week.                │
│ Black T-Shirt is your best-selling product.             │
│ Saturday was your busiest day.                          │
└─────────────────────────────────────────────────────────┘

┌──────────────────────────┐  ┌───────────────────────────┐
│ Sales Performance        │  │ Top Products              │
│                          │  │                           │
│          chart           │  │ Black T-Shirt   12 sold   │
│                          │  │ White T-Shirt    8 sold   │
│                          │  │ Blue Jeans       5 sold   │
└──────────────────────────┘  └───────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Financial Summary                                       │
│ Gross Sales       ₦520,000                              │
│ Returns           -₦35,000                              │
│ Net Sales          ₦485,000                             │
│ Collected          ₦350,000                             │
│ Outstanding        ₦135,000                             │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Recent Invoices                                         │
│ INV-1004  Sarah Johnson       ₦35,000       Paid        │
│ INV-1003  Michael Okafor      ₦50,000       Partial     │
└─────────────────────────────────────────────────────────┘
```

This is a **design reference and system of rules**, not a requirement to
reproduce the screenshots pixel-for-pixel.

------------------------------------------------------------------------

# 34. What SalesIQ Should Feel Like

When a business owner opens SalesIQ, the emotional progression should
be:

**"I can see my business."**

↓

**"I understand what happened."**

↓

**"I know what needs attention."**

↓

**"I can record my next sale easily."**

That is more important than any individual visual component.

The interface should make the product promise visible:

> **Know your sales. Grow your business.**

------------------------------------------------------------------------

# 35. Implementation Guidance

When implementing SalesIQ from this design reference:

-   Build reusable components.
-   Keep design tokens centralized.
-   Do not introduce arbitrary colors per screen.
-   Do not redesign individual pages independently.
-   Reuse the same card, button, input, badge, table, chart, and
    navigation patterns.
-   Preserve the desktop/mobile hierarchy.
-   Prefer progressive disclosure over showing everything at once.
-   Keep financial terminology consistent with the SalesIQ product
    definition.
-   Never introduce inventory terminology into MVP screens.
-   Never imply SalesIQ processes payments.
-   Use actual SalesIQ metrics and terminology rather than copying
    sample content from the reference screenshot.

## Most important rule

**Use the screenshots as the visual language, not as the product
specification.**

The reference establishes how SalesIQ should look and feel.

The SalesIQ product definition establishes what SalesIQ should
communicate.
