# SalesIQ — Product Requirements Document

## 1. Executive Product Overview

### 1.1 Product Vision

**SalesIQ** is a digital sales book and financial intelligence platform designed specifically for direct-to-consumer businesses, social commerce sellers (Instagram, WhatsApp, TikTok), and micro-enterprises operating in informal or direct-payment environments.

Instead of relying on unstructured chat histories, paper receipts, or bank alerts, SalesIQ enables business owners to effortlessly record completed sales, issue polished digital invoices/receipts, maintain reusable customer and product catalogs, and automatically transform raw transactions into actionable business intelligence.

### 1.2 Core Value Proposition

> **"Record every sale. Keep every transaction traceable. Understand your business."**

SalesIQ shifts business owners from high-friction, unorganized tracking to structured financial clarity:

* **From:** *"I know I made these sales, but I can't remember who owes what or what my best-selling item was."*
* **To:** *"Every sale has an identifiable digital record, my customers and catalog are organized, and my performance dashboard updates in real time."*

### 1.3 Target Audience & Persona

* **Primary User**: Business Owner / Founder / Sole Trader.
* **Operating Model**: Direct sales via WhatsApp, Instagram DM, phone calls, referrals, and physical transactions where payment collection happens directly between the seller and buyer prior to or upon delivery.
* **Authentication Hierarchy**:
    * **Business Owner**: First-class entity with full account authentication, configuration rights, and analytics access.
    * **Customers**: Secondary entities. They do **not** require accounts, logins, or passwords. They interact exclusively with read-only digital receipts sent to them via shareable web links or downloaded PDFs.



---

## 2. Global Platform Requirements & Principles

* **1:1 Business Scope**: Each authenticated user account is strictly tied to **one business profile** and **one business outlet**. Multi-business or multi-location management is explicitly out of scope for this version.
* **Offline-First Record Paradigm**: All sales captured on SalesIQ represent completed transactions that occurred outside the platform. The generated invoice functions as a **verified digital receipt** marked as **PAID**.
* **Zero-Block Friction**: Data entry flows (customers and products) feature inline creation and intelligent suggestions, eliminating rigid setup prerequisites before recording sales.

---

## 3. Detailed User Journeys & System Behavior

```
+-------------------------------------------------------------------------------------------------+
|                                    BUSINESS OWNER JOURNEY                                       |
+-------------------------------------------------------------------------------------------------+
| [1. Owner Signup]  --->  [2. Business Setup]  --->  [3. Empty-State Dashboard]                   |
| Personal Info           Mandatory & Optional        Action: "Record First Sale"                 |
|                                                                 |                               |
|                                                                 v                               |
| [6. Financial Briefing] <--- [5. Digital Receipt]  <---  [4. Sale Entry Flow]                      |
| Dashboard Intelligence        Public Link / PDF           Inline Customer & Product Autocomplete    |
+-------------------------------------------------------------------------------------------------+

```

---

### Journey 1: Authentication, Onboarding & Setup

#### 1.1 Account Registration (Owner Identity)

> **Goal**: Establish the business owner as the authenticated primary account holder.
* **Input Requirements**:
    * First Name & Last Name
    * Owner Email Address (Unique identifier)
    * Owner Phone Number
    * Account Password


* **Behavior**:
    * System validates email uniqueness and password security strength.
    * Upon submission, the owner profile is created, and the user is instantly guided into the Business Onboarding flow.



#### 1.2 Business Onboarding Flow

> **Goal**: Capture the operational details of the enterprise to personalize generated invoices and reports.

1. **Step A: Core Details (Mandatory)**
    * **Business Name**: Used on all customer-facing receipts and system headings.
    * **Business Phone Number**: Included in invoice footers for buyer inquiries.


2. **Step B: Profile & Branding Details (Optional / Skippable)**
* **Business Email**: Displays on receipts if different from personal email.
* **Business Address**: Physical address e.g (XXX XXXXX State, Country).
* **Business Logo** _(optional)_: Image upload for receipt branding.
* **Social Media Handles** _(optional)_: Instagram handle, WhatsApp store number, Facebook page link.
* **Default Currency**: Configurable currency symbol (e.g., `₦`, `$`).


**Behavior**:
* Owners can elect to "Skip for now" on optional branding fields and complete them later in Store Settings.
* No product catalog or customer entry is requested or forced during onboarding.



#### 1.3 Post-Onboarding First Landing (Clean Empty State)

> **Goal**: Encourage immediate engagement without overwhelming the owner with blank analytics.

**Behavior**:
* The user lands on the primary Dashboard in a clean **Empty State**.
* Analytics widgets display neutral indicators (`₦0.00 Total Revenue`, `0 Sales`).
* A prominent, visually prioritized Call-To-Action (CTA) banner reads: **`+ Record Your First Sale`**.


#### 1.4 Account Management, Security & Recovery

* **Login**: Email + Password authentication with standard "Remember Me" session backed-in.
* **Account Recovery (Forgot Password)** _(unaunthenticated user)_:
    1. Owner enters registered account email.
    2. System dispatches a secure password reset link valid for 60 minutes.
    3. Owner sets a new password and is redirected to the login screen.
* **Password Update** _(authenticated user)_:
    1. Owner navigates to security account settings
    2. Enter new password and confirm password correctness
    3. SalesIQ validates and approves the password update.

* **Logout**: Secure session termination, clearing local cached state, and redirecting to the login interface.

---

### Journey 2: Sales Recording & Invoice Generation Flow

#### 2.1 Initiating a Sale

* The owner clicks **`+ Record Sale`** or **`Create Invoice`** from any screen (Header, Sidebar, or Dashboard).
* A focused drawer or modal opens containing the invoice creation interface.

#### 2.2 Customer Entry & Intelligent Autocomplete

**Behavior**:
* As the owner types into the Customer Name or Phone field, SalesIQ evaluates the existing customer registry in real time.
* **Match Found**: Displays a dropdown list showing saved customer records (Name, Phone, Email). Selecting a customer auto-fills their associated contact details.
* **No Match Found (New Customer)**: The owner enters the new customer details (Name, Phone/Email). Upon saving the invoice, SalesIQ **automatically creates and persists** a new reusable customer record in the background without interrupting the flow.



```
Customer Input: "Adesola"
               |
               +--> [ Search Customer DB ] (passive)
                        |
                        +-- Match Found?
                        |    |--> YES: Show dropdown suggestion -> Select & Auto-fill
                        |    |--> NO:  Continue typing -> Save on completion -> Re-useable Customer Record

```

#### 2.3 Line-Item Selection & Product Catalog Interaction

**Behavior**:
* The owner begins typing a product name in the invoice line item field.
* **Match Found**: SalesIQ suggests matching catalog products showing saved product names and default base prices.
    * **One-Off Price Adjustment**:
        * If the item is sold at a custom rate (e.g., custom discount given over Instagram DM), the owner can manually edit the unit price directly on the invoice line item.
        * **Catalog Integrity Rule**: Editing the price on a specific invoice line item applies **only** to that transaction. It does **not** alter the saved base price in the global product catalog.





            ```
            Product Input: "Silk Scarf" (Base Catalog Price: $50)
                        |
                        +--> Owner changes line item price to $45 for this sale.
                        |
                        +--> RESULT: 
                                * Invoice total calculated using $45.
                                * Catalog Base Price remains $50 for future sales.

            ```

    * **Price Increase & Catalog Update Prompt**: If the owner enters a price **higher** than the saved base price for an existing product, SalesIQ triggers a contextual prompt before receipt generation:
        > *"You entered a higher price (₦15,000) than your catalog base price (₦12,000). Would you like to update the catalog price for future sales?"*


    * **If Accepted (`Yes`)**: The catalog base price is updated to ₦15,000.
    * **If Declined (`No`)**: The catalog base price remains ₦12,000. The invoice is generated with ₦15,000.


* **New Product Auto-Creation**: If a non-existent product is typed, SalesIQ registers the new item, sets its entered price as the default base catalog price, and persists it to the database upon invoice creation.



#### 2.4 Taxes, Discounts & Summary Calculation

* **Discounts**: Flat amount or percentage discount applied to the overall subtotal.
* **Tax / VAT**: Toggleable tax field with optional percentage rule (e.g., 7.5% VAT).
* **Summary Real-Time Recalculation**: Subtotal, Applied Tax, Total Discount, and Final Grand Total update dynamically as items are edited.

#### 2.5 Invoice Finalization

* The owner clicks **`Generate Paid Invoice`**.
* The transaction is immediately committed to the digital sales book as a **PAID** transaction with a unique transaction reference ID (e.g., `INV-2026-0891`).

---

### Journey 3: Digital Receipt & Customer Experience

#### 3.1 Receipt Delivery Options

Once the invoice is generated, the owner is presented with a success notification and instant sharing controls:

* **`Copy Digital Link`**: Copies a unique public URL (`[https://app.salesiq.com.ng/r/inv-2026-0891](https://app.salesiq.com.ng/r/inv-2026-0891)`).
* **`Share via WhatsApp`**: Opens WhatsApp with a pre-formatted message:
> *"Hello [Customer Name], thank you for your business! Here is your official receipt from [Business Name]: [https://app.salesiq.com.ng/r/inv-2026-0891](https://www.google.com/url?sa=E&source=gmail&q=https://app.salesiq.com.ng/r/inv-2026-0891)"*


* **`Download PDF`**: Generates a standard high-resolution PDF file formatted for saving or printing.

#### 3.2 Customer-Facing Digital Receipt Page

* **Access Control**: Publicly accessible via unique URL token. No customer login required.
* **View & Behavior**:
    * **Read-Only Visuals**: Formatted as a professional digital receipt featuring the business logo, business contact info, transaction date, unique invoice ID, itemized breakdown, taxes, and final total.
* **Status Badge**: Prominently displays a green **`PAID`** stamp.
* **Customer Actions**: 
    * Single clear CTA: **`Download PDF Receipt`**.
* **No Payment Gateway**: Because payment occurred offline prior to record creation, there are no interactive payment inputs on this receipt page.



---

### Journey 4: Dashboard & Business Intelligence Outcomes

#### 4.1 Real-Time Intelligence Aggregation

Every completed sale instantly updates the core business intelligence engine, transforming isolated transactions into aggregated briefs without requiring manual calculation.

#### 4.2 Key Performance Indicators (KPI Briefing)

The dashboard acts as an automated morning briefing for the business owner:

* **Total Sales Revenue**: Cumulative monetary value of recorded sales over chosen timeframes (Today, Last 7 Days, This Month, Year to Date).
* **Total Orders Recorded**: Total count of completed transactions.
* **Average Sale Value (ASV)**: Calculated as $\text{Total Revenue} \div \text{Total Sales Count}$.
* **Comparison Benchmarks**: Inline metrics showing growth or decline compared to previous equal periods (e.g., `+14.2% vs. last week`).

#### 4.3 Analytics Modules & Visual Insights

* **Revenue Performance Chart**: Visual line/area chart showing daily and weekly revenue trends to identify high-volume sales days.
* **Best-Selling Products Widget**: Ranked list of top products by total volume sold and total revenue generated, helping owners understand what inventory drives performance.
* **Busiest Sales Days**: Frequency breakdown indicating peak sales days (e.g., "Saturdays generate 38% of weekly revenue").
* **Customer Transaction History**: List of top customers sorted by purchase frequency and total lifetime value.

---

## 4. Feature Behavior Summary Table

| Feature Area | Trigger / User Action | System Behavior & Logic | Output / Result |
| --- | --- | --- | --- |
| **Customer Lookup** | Typing name or phone number during sale entry | Real-time lookup in customer database. Displays dropdown matching existing records. | Auto-fills customer profile or tags new customer for auto-creation on save. |
| **Product Autocomplete** | Typing product title during sale entry | Queries product catalog. Fills base price into invoice line item. | Line item populated quickly without breaking typing momentum. |
| **Manual Price Edit** | Overriding unit price on an invoice line item | Modifies line item calculation for current invoice. Leaves global catalog base price untouched. | Custom one-off price or discount applied to current invoice only. |
| **Price Increase Detect** | Entering a price higher than catalog base price | Triggers inline modal prompt asking if base catalog price should be updated. | Updates catalog base price if confirmed (`Yes`); keeps original base price if declined (`No`). |
| **Receipt Generation** | Clicking `Generate Paid Invoice` | Writes sale to DB, increments revenue metrics, and creates unique public web receipt link. | Displays success modal with WhatsApp share button and PDF download link. |
| **Public Receipt Access** | Customer opening shared URL | Renders lightweight, mobile-responsive read-only digital receipt with `PAID` status. | Customer views official receipt and can click `Download PDF`. |
| **Dashboard Briefing** | Owner opening application homepage | Aggregates all recorded sales records into KPI blocks, charts, and product rankings. | Instant visual summary of business health, average order value, and revenue growth. |

---

## 5. Non-Functional Product Expectations

* **Zero-Lag Input**: Customer and product autocomplete search results must appear within under 100 milliseconds to maintain fluid manual entry.
* **Mobile First Operational Ergonomics**: Since many social commerce merchants manage their businesses entirely from smartphones, all record creation and receipt sharing flows must be 100% optimized for single-handed mobile browser execution.
* **URL Resilience**: Public receipt links must remain permanently accessible via secure, unguessable cryptographic hash tokens.