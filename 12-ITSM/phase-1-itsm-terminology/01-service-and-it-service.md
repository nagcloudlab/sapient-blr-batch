# Section 1: Service & IT Service

## What is a Service?

A way to deliver **value** to customers by helping them achieve outcomes they want, *without them owning the costs and risks*.

Simple: **"I give you something useful. You don't worry about how it works."**

---

## UPI Example

When you open GPay and send Rs.500 to a friend:

- You don't know which servers processed it
- You don't care about NPCI's data centers
- You don't manage the network between banks

**You just want: money moved, instantly, reliably.** That's a **service**.

---

## IT Service vs Business Service

| Type | Example | Who sees it? |
|---|---|---|
| **Business Service** | "UPI Payments" -- send/receive money | End users (you, merchants) |
| **IT Service** | UPI Transaction Processing Engine | Internal NPCI teams |
| **Infrastructure Service** | Database cluster, Kafka messaging, Load balancers | Ops/Platform teams |

They stack like a pyramid:

```
        End User sees:
       +-------------------+
       |  Business Service  |  <-- "UPI Payments"
       +---------+---------+
                 | depends on
       +---------v---------+
       |    IT Service      |  <-- Transaction Engine, Settlement Engine
       +---------+---------+
                 | depends on
       +---------v---------+
       |  Infrastructure    |  <-- Servers, DBs, Network, Kafka
       +-------------------+
```

**When the DB goes down (infra) -> Transaction Engine breaks (IT service) -> Users can't pay (business service).**

That chain is why ITSM matters -- you manage bottom-up so the top stays healthy.

---

## Examples of IT Services at NPCI

| IT Service | What it does |
|---|---|
| **UPI Transaction Processing** | Routes payment from sender bank -> receiver bank |
| **UPI Registration Service** | Links mobile number -> bank account -> VPA (yourname@upi) |
| **Dispute Resolution Service** | Handles failed/stuck transactions, refunds |
| **Settlement Service** | End-of-day money movement between banks |
| **Merchant Onboarding** | Registers PhonePe, GPay, Paytm as UPI apps |

---

## Key Terms

| Term | Meaning | UPI Example |
|---|---|---|
| **Service** | Delivers value without exposing complexity | UPI Payments |
| **Service Provider** | Org that delivers the service | NPCI |
| **Service Consumer** | Org/person that uses the service | Banks, PhonePe, end users |
| **Outcome** | What the consumer actually wants | "Money transferred instantly" |
| **Output** | What the provider produces | Transaction ID, confirmation |
| **Value** | Perceived benefit by consumer | Trust, speed, convenience |

---

## Discussion

> If NPCI's UPI is down for 30 minutes during peak hours (lunch time), what's the business impact?
> - ~8 million failed transactions
> - Merchants can't accept payments
> - Consumer trust drops
> - RBI scrutiny
>
> This is why we don't just "run servers" -- we **manage services**.
