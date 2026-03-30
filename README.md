# 🚗 EcoRoute - Smart Carpooling & Task Management

**EcoRoute** هو منصة ويب متكاملة مبنية باستخدام **Flask**، تهدف لتنظيم الرحلات المشتركة (Carpooling) وإدارة المهام والاشتراكات بشكل ذكي وآمن.

## 🌟 المميزات الرئيسية (Features)
* **نظام إدارة المستخدمين:** تسجيل دخول، وتشفير كلمات السر باستخدام `Bcrypt`.
* **لوحة تحكم كاملة (Admin Panel):** تحكم في المستخدمين، السيارات، والرحلات مع نظام صلاحيات صارم.
* **إدارة الرحلات:** إمكانية إضافة وحجز الرحلات وتتبع الاشتراكات.
* **حماية البيانات:** تطبيق نظام الـ Roles (Admin vs User) لمنع الدخول غير المصرح به.

## 🛠 التكنولوجيات المستخدمة (Tech Stack)
* **Backend:** Python (Flask Framework)
* **Database:** SQLAlchemy (SQLite/PostgreSQL)
* **Security:** Flask-Login & Flask-Bcrypt
* **Interface:** Flask-Admin & Jinja2 Templates

## 🚀 كيفية التشغيل (Setup)
1. قم بتحميل المشروع (Clone):
   ```bash
   git clone [https://github.com/your-username/EcoRoute.git](https://github.com/your-username/EcoRoute.git)