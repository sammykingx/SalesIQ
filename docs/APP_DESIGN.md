# SalesIQ — Design System & Visual Specification

This document serves as the canonical Design System & UI Specification for **SalesIQ**. It defines the visual identity, UI components, interaction patterns, layout structures, and design tokens needed to ensure absolute design consistency across light and dark modes during development.

---

## 1. Design Philosophy & Aesthetic Vision

SalesIQ’s aesthetic merges the structured clarity of modern modern SaaS dashboards (inspired by Linear, Vercel, and Stripe) with the vibrant, approachable warmth of modern fintech platforms.

### Core Visual Principles

* **High Information Density & Scannability**: High contrast hierarchy, tight typography leading, and zero layout bloat. Business owners can review performance in under 3 seconds.
* **Glassmorphism & Depth**: Multi-layered depth achieved through subtle ambient glows (`backdrop-blur`), soft border outlines (`1px solid border`), and soft dropshadows instead of heavy solid backgrounds.
* **Dual-Mode Harmony**: Native light and dark themes where colors are functionally mapped (not just inverted), maintaining visual warmth and comfort in low-light environments.
* **Micro-Data Rich**: Key metrics are paired with subtle sparklines, percentage pill badges, and contextual comparison indicators (e.g., `+12.4% vs. previous period`).

---

## 2. Color System & Design Tokens

### 2.1 Brand Color Palette (From Brand Guidelines)

* **Primary Emerald (`#10B981` / `#0EA5E9` gradient)**: Primary action, revenue growth, active states.
* **Deep Indigo (`#0F172A` / `#0B132B`)**: Primary text in light mode, background surfaces in dark mode.
* **Accent Electric Blue (`#6366F1`)**: Financial cards, specialized metrics, highlights.
* **Accent Sky Blue (`#0EA5E9`)**: Informational indicators, secondary chart lines.
* **Neutral Off-White (`#F8FAFC`)**: Canvas background in light mode.

### 2.2 Functional Color Mapping

| Token | Light Mode Value | Dark Mode Value | Usage / Application |
| --- | --- | --- | --- |
| **`--bg-app`** | `#F8FAFC` | `#080C14` | Base application background |
| **`--bg-surface`** | `#FFFFFF` | `#0F172A` | Standard card containers, tables, modals |
| **`--bg-surface-elevated`** | `#F1F5F9` | `#1E293B` | Hover states, secondary action wells |
| **`--border-subtle`** | `rgba(226, 232, 240, 0.8)` | `rgba(255, 255, 255, 0.08)` | Card borders, table dividers |
| **`--border-focus`** | `rgba(16, 185, 129, 0.5)` | `rgba(16, 185, 129, 0.5)` | Input highlight, focused states |
| **`--text-primary`** | `#0F172A` | `#F8FAFC` | Main headings, key values |
| **`--text-secondary`** | `#64748B` | `#94A3B8` | Body text, section labels, timestamps |
| **`--text-muted`** | `#94A3B8` | `#64748B` | Placeholders, inactive labels |
| **`--accent-green`** | `#10B981` | `#34D399` | Revenue cards, positive trend badges (`+12.4%`) |
| **`--accent-green-glow`** | `rgba(16, 185, 129, 0.12)` | `rgba(52, 211, 153, 0.15)` | Background pill tags for positive metrics |
| **`--accent-red`** | `#EF4444` | `#F87171` | Negative trend badges (`-3.1%`), delete actions |
| **`--accent-red-glow`** | `rgba(239, 68, 68, 0.12)` | `rgba(248, 113, 113, 0.15)` | Negative pill background |

---

## 3. Typography & Hierarchy

**Font Family**: `Inter`, system-ui, -apple-system, sans-serif.

### Scale & Hierarchy Table

| Level | Size / Line Height | Weight | Style / Tracking | Usage |
| --- | --- | --- | --- | --- |
| **Display Header** | `28px / 36px` | Bold (`700`) | `-0.02em` | Page Titles (e.g., "Sales", "Dashboard") |
| **Section Title** | `18px / 24px` | SemiBold (`600`) | `-0.01em` | Card Block titles (e.g., "Sales Overview") |
| **Metric Hero** | `32px / 40px` | Bold (`700`) | `-0.03em` | Major revenue numbers (`₦1,250,000`) |
| **Metric Standard** | `20px / 28px` | Bold (`700`) | `-0.02em` | Grid metrics (`3,920`, `1,204`) |
| **Body Large** | `15px / 22px` | Regular (`400`) | Normal | Descriptive subtitles, welcome messages |
| **Body Regular** | `13px / 18px` | Regular (`400`) | Normal | Table text, form labels, secondary details |
| **Caption / Label** | `11px / 16px` | Medium (`500`) | `+0.05em` UPPERCASE | Overline labels (e.g., `SALES OVERVIEW`, `PERFORMANCE`) |

---

## 4. Layout Architecture & Structure

The shell uses a persistent collapsible **Iconic Left Sidebar**, a **Top Utility Command Bar**, and a **Fluid Canvas Content Area**.

```
+-----------------------------------------------------------------------------------+
| [S] | [Q Search or jump to... K]                    [EN] [🌙] [🔔] [User Avatar] |
+-----+-----------------------------------------------------------------------------+
| [⊞] | Breadcrumbs > Sales                                                       |
| [📊]|                                                                           |
| [🛒]|  # Sales                                                                  |
| [👥]|  Here's how revenue is tracking — Jul 2025 to Jun 2026.                   |
| [🏷️]|                                                                           |
| [📄]|  +---------------------------------------+ +----------------------------+ |
| [⚙️]|  | Hero Welcome & Quick Action Card      | | Total Revenue Spotlight   |  |
|     |  +---------------------------------------+ +----------------------------+ |
|     |  +----------------------------------------------------------------------+ |
|     |  | Metric Row (Customers | Products | Transactions | Avg Order Value)   | |
|     |  +----------------------------------------------------------------------+ |
|     |  +---------------------------------------+ +----------------------------+ |
|     |  | Sales Statistics Chart Area           | | Balance / Financial Wallet | |
|     |  +---------------------------------------+ +----------------------------+ |
+-----+---------------------------------------------------------------------------+

```

### 4.1 Navigation Sidebar

* **Width**: Collapsed `64px`, Expanded `240px`.
* **Behavior**: Hovering or clicking expand toggle unrolls clean text labels alongside icons.
* **Active State**: Primary background glow pill behind icon + indicator line on the left edge.
* **Items**:
1. `Dashboard` (Overview metrics)
2. `Sales / Invoices` (Sales recording & digital sales book)
3. `Products` (Reusable product catalog)
4. `Customers` (Reusable customer directory & history)
5. `Reports & Analytics` (Business intelligence)
6. `Settings` (Store profile, currency, taxes)



### 4.2 Top Utility Bar

* **Global Search (`Cmd + K`)**: Pill-shaped input field with keyboard shortcut badge. Searches across customers, products, and invoice IDs simultaneously.
* **Action Cluster**: Quick Language Switcher (`EN`), Light/Dark Mode Toggle (`☀️/🌙`), Notifications (`🔔` with active count badge), and Profile Avatar.

---

## 5. UI Component Specifications (Inspired by Layout Screenshots)

### 5.1 Hero Welcome & Quick Action Card

* **Layout**: Left side features personalized greeting, smart brief summary, and prominent action button; right side highlights target completion stats.
* **Components**:
* **Primary Action**: Brand Green Button (`Create Invoice` / `Record Sale`) with icon + glow shadow.
* **Secondary Action**: Subtle Outline Button (`View Pipeline` / `All Invoices`).
* **Stat Columns**: Compact inline metrics (`Target hit: 86%`, `Deals won: 142`, `Still open: 37`).



### 5.2 Spotlight Revenue Card (Emerald Card)

* **Background**: Solid Emerald Green (`#10B981` light mode, `#059669` dark mode) with a subtle radial gradient mesh.
* **Content**: Large Hero Metric (`₦748.2K` or `$748.2K`), Trend Pill (`▲ 12.4% vs. previous year`), and an organic smoothed line sparkline chart anchored to the bottom.

### 5.3 Metric Horizontal Strip

* **Structure**: A 4-column or 5-column grid section with thin vertical dividers (`--border-subtle`).
* **Each Metric Cell Contains**:
* Icon inside a soft-colored rounded box (`32x32px`).
* Upper Label (`Customers`, `Products`, `Transactions`, `Avg. order value`).
* Big Value (`3,920`, `1,204`, `₦76.24`).
* Inline Percentage Pill Badge (`-3.1%`, `+2.0%`).



### 5.4 Data Visualization & Chart Styling

* **Chart Type**: Smooth Area Curve Chart with gradient fill under the line fading to `0%` opacity.
* **Dual Datasets**:
* **Primary (Current Period)**: Vibrant Green/Cyan line (`#10B981`).
* **Secondary (Previous Period)**: Muted Blue/Gray dashed or low-opacity line (`#0EA5E9`).


* **Interactions**: Hovering reveals an interactive vertical hair-line crosshair and a high-contrast floating tooltip listing exact transaction counts and totals.

### 5.5 Accent Financial Balance Card

* **Aesthetic**: Modern digital card aesthetic using a soft purple-blue gradient background (`linear-gradient(135deg, #6366F1, #A855F7)`).
* **Details**: Currency selector pills (`NGN`, `USD`, `GBP`), available balance readout, and masked account/reference identifier (`4921 •••• •••• 7845`).

---

## 6. Primary Feature Screens & UI Wireframe Specs

### 6.1 "Record Sale / Invoice" Flow

* **Trigger**: Prominent floating or header button `+ Record Sale`.
* **Modal / Drawer Layout**:
1. **Customer Selector**: Combobox search field ("Search customer by name or phone..."). Includes a quick `+ Add New Customer` inline button.
2. **Line Items Table**: Dynamic list allowing quick product searches from catalog or manual item entry. Automatically calculates line subtotal based on quantity, unit price, and discount.
3. **Financial Summary Block**: Clean breakdown of Subtotal, VAT/Tax toggles, Discount deductions, and Grand Total.
4. **Payment Status Switcher**: Visual segmented tab control: `[ Paid ]` | `[ Partial ]` | `[ Unpaid / Pending ]`.
5. **Footer Actions**:
* Primary: `Save & Generate Invoice` (Green solid button).
* Secondary: `Share via WhatsApp` (Direct green outline icon button).





### 6.2 Customer & Product Table Views

* **Header**: Filter bar with search, status dropdown filter, date picker range (`Last 30 days`), and `Export` CSV button.
* **Row Design**: Alternating subtle hover highlighting (`--bg-surface-elevated`).
* **Status Badges**:
* **Paid / Completed**: Green background pill with dark green text.
* **Pending / Outstanding**: Amber background pill with orange text.
* **Overdue**: Red background pill with red text.



---

## 7. Responsive & Micro-Interaction Guidelines

### 7.1 Breakpoints

* **Mobile (`< 640px`)**:
* Sidebar transitions into a bottom navigation bar or hamburger drawer.
* Metrics strip converts from horizontal 4-column layout into a 2x2 grid.
* Floating Action Button (FAB) at bottom-right for quick `+ Record Sale`.


* **Tablet (`640px - 1024px`)**:
* Sidebar stays in collapsed iconic mode (`64px`).
* Hero cards stack vertically.


* **Desktop (`> 1024px`)**:
* Full dashboard grid with side-by-side hero metrics and statistics charts.



### 7.2 Micro-Interactions & Transitions

* **Hover States**: All clickable cards and metric tiles feature a subtle upward translate transform (`translateY(-2px)`) with a 200ms ease-out transition.
* **Theme Switching**: Smooth theme transition (`background-color 0.3s ease, color 0.3s ease`) when toggling between Light and Dark mode.
* **State Indicators**: Live pulses on active status badges (e.g., green dot pulsing next to "Real-time updates active").