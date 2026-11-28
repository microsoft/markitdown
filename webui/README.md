# MarkItDown Web UI

واجهة ويب بسيطة فوق مكتبة MarkItDown: اسحب الملفات وأفلتها، وتتحول إلى Markdown مع معاينة ونسخ وتنزيل.

## التشغيل على السيرفر (Docker)

من جذر الريبو:

```bash
docker compose -f webui/docker-compose.yml up -d --build
```

ثم افتح `http://SERVER_IP:8000`.

## المتغيرات (docker-compose.yml)

| المتغير | الافتراضي | الوصف |
|---|---|---|
| `MAX_UPLOAD_MB` | `50` | الحد الأقصى لحجم الملف |
| `AUTH_USER` / `AUTH_PASSWORD` | فارغ | إذا حددت كلمة المرور، تُطلب عند فتح الصفحة (HTTP Basic) |

> إذا السيرفر مفتوح للإنترنت، فعّل `AUTH_PASSWORD` وضعه خلف HTTPS (Caddy / Nginx / Cloudflare Tunnel).

## التشغيل بدون Docker

```bash
pip install "./packages/markitdown[all]" -r webui/requirements.txt
cd webui && uvicorn app:app --host 0.0.0.0 --port 8000
```

## ملاحظات

- الملفات تُعالج في ملف مؤقت ويُحذف مباشرة، ولا يُحفظ شيء على السيرفر.
- الإضافات (plugins) وتحويل الروابط من السيرفر معطلة عمدًا لأسباب أمنية.
- الصور والصوت تحتاج إعدادات إضافية في MarkItDown (OCR / خدمة LLM)، وبدونها يُستخرج الوصف الفوقي (metadata) فقط.
