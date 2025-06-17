# Pravi Foods – Supply Chain Management System (SCMS) MVP Architecture

## Overview
This document outlines a modular agent-based architecture for a B2B Supply Chain Management System for Arivu Foods. The MVP focuses on automating operations between FMCG admins and local retail stores using Python and FastAPI.

## Key Modules
- **Inventory Tracking & Reorder Logic**: Track stock levels and trigger automated reorder suggestions.
- **Order Lifecycle Management**: Handle order creation, approval, and fulfillment.
- **Retailer CRM & Terms**: Store credit limits, contract terms, and contacts for each retail store.
- **Invoice & Billing**: Auto-generate invoices upon order fulfillment with payment tracking.
- **Analytics & Dashboards**: Present KPIs for sales, stock, and performance in a web dashboard.
- **Notifications**: Send email/SMS alerts for order status and low stock.
- **Audit & Roles**: Maintain audit logs and enforce role-based access.

## Agents
- **Order Agent**: Manages order state transitions and inventory adjustments.
- **Inventory Agent**: Monitors stock, triggers reorder tasks, and syncs with the warehouse.
- **CRM Agent**: Handles retailer data, credit limits, and terms.
- **Billing Agent**: Generates invoices and records payments.
- **Analytics Agent**: Aggregates data for dashboards and reporting.

## Tech Stack
- **Backend**: Python + FastAPI with Pydantic models.
- **Database**: PostgreSQL or SQLite for MVP.
- **Messaging**: Celery/RabbitMQ for asynchronous tasks and notifications.
- **Frontend**: Minimal dashboard using FastAPI templates or a JS framework.

## User Roles
1. **FMCG Admin**
   - Manage products, pricing, inventory thresholds, and credit limits.
   - Approve or monitor orders, or configure auto-processing rules.
   - Access full analytics and billing features.
2. **Local Retail Store**
   - Place and track orders.
   - View invoices and product catalog.
   - Analyze order trends via dashboard (limited to their data).

## MVP Flow
1. Retailer places an order via the dashboard or API.
2. Order Agent validates stock and forwards for approval if needed.
3. Inventory Agent deducts reserved stock and alerts if thresholds are breached.
4. Billing Agent issues invoice upon shipment.
5. Analytics Agent updates KPIs and dashboard metrics.
6. Notifications are dispatched for major events (order confirmation, shipment, invoice).

