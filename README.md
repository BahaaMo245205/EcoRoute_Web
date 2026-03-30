# 🚗 EcoRoute - Smart Carpooling & Task Management

**EcoRoute** هي منصة ويب متطورة تهدف إلى تسهيل عملية مشاركة الرحلات (Carpooling) وإدارة المهام المرتبطة بها بشكل آمن وفعال. تم بناء النظام بالتركيز على تجربة المستخدم (UX) ومعايير الأمان العالية.

---

## 🌟 المميزات الرئيسية (Key Features)

- **🔐 نظام أمان متقدم:**
    
    - تشفير كلمات المرور باستخدام خوارزمية `Bcrypt`.
        
    - إدارة الجلسات (Sessions) باستخدام `Flask-Login`.
        
    - نظام صلاحيات (Role-Based Access Control) يفرق بين المسؤولين (Admins) والمستخدمين.
        
- **🏗️ لوحة تحكم إدارية (Custom Admin Dashboard):**
    
    - واجهة مخصصة مبنية بـ `Flask-Admin`.
        
    - تحكم كامل في قواعد البيانات (Users, Cars, Trips, Bookings).
        
    - منع الوصول لغير المصرح لهم برمجياً عبر الـ `is_accessible`.
        
- **📅 إدارة الرحلات والاشتراكات:**
    
    - نظام ذكي لحجز الرحلات وتتبع حالة العربيات والركاب.
        
- **💻 بنية برمجية منظمة:**
    
    - استخدام الـ `Blueprints` لتنظيم الأكواد وتسهيل التوسع في المشروع (Scalability).
        

---

## 🛠 التكنولوجيات المستخدمة (Tech Stack)

|**Category**|**Technology**|
|---|---|
|**Backend**|Python & Flask Framework|
|**Database**|SQLAlchemy (ORM) with SQLite/PostgreSQL|
|**Security**|Flask-Bcrypt (Hashing) & Flask-Login|
|**Admin UI**|Flask-Admin (Bootstrap 3 templates)|
|**Architecture**|MVC Pattern & Blueprints|

---

## 🚀 كيفية التشغيل (Quick Start)

## 1. المتطلبات (Prerequisites)

تأكد من تثبيت **Python 3.12+** على جهازك.

## 2. التثبيت (Installation)

قم بتحميل المشروع وتهيئة البيئة الافتراضية:

Bash

```
# Clone the repository
git clone https://github.com/your-username/EcoRoute.git
cd EcoRoute

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. تشغيل التطبيق (Running)

Bash

```
python app.py
```

> سيظهر التطبيق على الرابط: `http://127.0.0.1:5000`